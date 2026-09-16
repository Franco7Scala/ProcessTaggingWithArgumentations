 /*!
 * Copyright (c) <2020> <Andreas Niskanen, University of Helsinki>
 * 
 * 
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * 
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * 
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include "Encodings.h"
#include "Util.h"
#include "CountExtensions.h"

using namespace std;

namespace CountExtensions {

uint32_t complete(const AF & af)
{
	SAT_Solver solver = SAT_Solver(af.count, af.args);
	Encodings::add_complete(af, solver);
	uint32_t count = 0;
	while (true) {
		bool sat = solver.solve();
		if (!sat) break;
		vector<int> blocking_clause(af.args);
		for (uint32_t i = 0; i < af.args; i++) {
			if (solver.assignment[af.accepted_var[i]-1]) {
				blocking_clause[i] = -af.accepted_var[i];
			} else {
				blocking_clause[i] = af.accepted_var[i];
			}
		}
		count++;
		solver.add_clause(blocking_clause);
	}
	return count;
}

uint32_t preferred(const AF & af)
{
	SAT_Solver solver = SAT_Solver(af.count, af.args);
	Encodings::add_complete(af, solver);
	uint32_t count = 0;
	while (true) {
		bool sat = solver.solve();
		if (!sat) break;
		vector<int> complement_clause;
		complement_clause.reserve(af.args);
		vector<int> assumptions;
		assumptions.reserve(af.args);
		vector<uint8_t> visited;
		visited.resize(af.args);
		while (true) {
			complement_clause.clear();
			for (uint32_t i = 0; i < af.args; i++) {
				if (solver.assignment[af.accepted_var[i]-1]) {
					if (!visited[i]) {
						assumptions.push_back(af.accepted_var[i]);
						visited[i] = true;
					}
				} else {
					complement_clause.push_back(af.accepted_var[i]);
				}
			}
			solver.add_clause(complement_clause);
			bool superset = solver.solve(assumptions);
			if (!superset) break;
		}
		count++;
	}
	return count;
}

uint32_t stable(const AF & af)
{
	SAT_Solver solver = SAT_Solver(af.count, af.args);
	Encodings::add_stable(af, solver);
	uint32_t count = 0;
#if defined(GR_IN_ST)
	vector<int> assumptions = grounded_assumptions(af);
	for (uint32_t i = 0; i < assumptions.size(); i++) {
		vector<int> clause = { assumptions[i] };
		solver.add_clause(clause);
	}
#endif
	while (true) {
		bool sat = solver.solve();
		if (!sat) break;
		vector<int> blocking_clause;
		blocking_clause.reserve(af.args);
		for (uint32_t i = 0; i < af.args; i++) {
			if (!solver.assignment[af.accepted_var[i]-1]) {
				blocking_clause.push_back(af.accepted_var[i]);
			}
		}
		count++;
		solver.add_clause(blocking_clause);
	}
	return count;
}

uint32_t semi_stable(const AF & af)
{
	SAT_Solver solver = SAT_Solver(af.count, 2*af.args);

	Encodings::add_complete(af, solver);
	Encodings::add_range(af, solver);
	uint32_t count = 0;

#if defined(ST_EXISTS_SST)
	vector<int> range_assumption(af.args);
	for (uint32_t i = 0; i < af.args; i++) {
		range_assumption[i] = af.range_var[i];
	}
	bool stb_exists = false;
	while (solver.solve(range_assumption)) {
		if (!stb_exists) {
			stb_exists = true;
		}
		vector<int> blocking_clause;
		blocking_clause.reserve(af.args);
		for (uint32_t i = 0; i < af.args; i++) {
			if (!solver.assignment[af.accepted_var[i]-1]) {
				blocking_clause.push_back(af.accepted_var[i]);
			}
		}
		count++;
		solver.add_clause(blocking_clause);
	}
	if (stb_exists) {
		return count;
	}
#endif

	while (true) {
		bool sat = solver.solve();
		if (!sat) break;

		vector<int> complement_clause;
		complement_clause.reserve(af.args);

		vector<int> assumptions;
		assumptions.reserve(af.args);

		vector<uint8_t> visited;
		visited.resize(af.args);

		while (true) {
			complement_clause.clear();
			for (uint32_t i = 0; i < af.args; i++) {
				if (solver.assignment[af.range_var[i]-1]) {
					if (!visited[i]) {
						assumptions.push_back(af.range_var[i]);
						visited[i] = true;
					}
				} else {
					complement_clause.push_back(af.range_var[i]);
				}
			}
			solver.add_clause(complement_clause);
			bool superset = solver.solve(assumptions);
			if (!superset) break;
		}

		assumptions.resize(af.args);
		for (uint32_t i = 0; i < af.args; i++) {
			if (visited[i]) {
				assumptions[i] = af.range_var[i];
			} else {
				assumptions[i] = -af.range_var[i];
			}
		}
		
		SAT_Solver new_solver(af.count, af.args);

		Encodings::add_complete(af, new_solver);
		Encodings::add_range(af, new_solver);

		while (true) {
			bool sat = new_solver.solve(assumptions);
			if (!sat) break;
			vector<int> blocking_clause;
			blocking_clause.reserve(af.args);
			for (uint32_t i = 0; i < af.args; i++) {
				if (!new_solver.assignment[af.accepted_var[i]-1]) {
					blocking_clause.push_back(af.accepted_var[i]);
				}
			}
			count++;
			new_solver.add_clause(blocking_clause);
		}
	}
	return count;
}

uint32_t stage(const AF & af)
{
	SAT_Solver solver = SAT_Solver(af.count, 2*af.args);

	Encodings::add_conflict_free(af, solver);
	Encodings::add_range(af, solver);
	uint32_t count = 0;

#if defined(ST_EXISTS_STG)
	vector<int> range_assumption(af.args);
	for (uint32_t i = 0; i < af.args; i++) {
		range_assumption[i] = af.range_var[i];
	}
	bool stb_exists = false;
	while (solver.solve(range_assumption)) {
		if (!stb_exists) {
			stb_exists = true;
		}
		vector<int> blocking_clause;
		blocking_clause.reserve(af.args);
		for (uint32_t i = 0; i < af.args; i++) {
			if (!solver.assignment[af.accepted_var[i]-1]) {
				blocking_clause.push_back(af.accepted_var[i]);
			}
		}
		count++;
		solver.add_clause(blocking_clause);
	}
	if (stb_exists) {
		return count;
	}
#endif

	while (true) {
		bool sat = solver.solve();
		if (!sat) break;

		vector<int> complement_clause;
		complement_clause.reserve(af.args);

		vector<int> assumptions;
		assumptions.reserve(af.args);

		vector<uint8_t> visited;
		visited.resize(af.args);

		while (true) {
			complement_clause.clear();
			for (uint32_t i = 0; i < af.args; i++) {
				if (solver.assignment[af.range_var[i]-1]) {
					if (!visited[i]) {
						assumptions.push_back(af.range_var[i]);
						visited[i] = true;
					}
				} else {
					complement_clause.push_back(af.range_var[i]);
				}
			}
			solver.add_clause(complement_clause);
			bool superset = solver.solve(assumptions);
			if (!superset) break;
		}

		assumptions.resize(af.args);
		for (uint32_t i = 0; i < af.args; i++) {
			if (visited[i]) {
				assumptions[i] = af.range_var[i];
			} else {
				assumptions[i] = -af.range_var[i];
			}
		}
		
		SAT_Solver new_solver(af.count, af.args);

		Encodings::add_conflict_free(af, new_solver);
		Encodings::add_range(af, new_solver);

		while (true) {
			bool sat = new_solver.solve(assumptions);
			if (!sat) break;
			vector<int> blocking_clause;
			blocking_clause.reserve(af.args);
			for (uint32_t i = 0; i < af.args; i++) {
				if (!new_solver.assignment[af.accepted_var[i]-1]) {
					blocking_clause.push_back(af.accepted_var[i]);
				}
			}
			count++;
			new_solver.add_clause(blocking_clause);
		}
	}
	return count;
}

}