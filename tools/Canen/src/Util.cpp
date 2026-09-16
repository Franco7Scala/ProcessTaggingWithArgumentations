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

#include <iostream>

#include "Encodings.h"
#include "Util.h"

using namespace std;

vector<int> grounded_assumptions(const AF & af)
{
	SAT_Solver solver = SAT_Solver(af.count, 2*af.args);
	Encodings::add_complete(af, solver);
	bool sat = solver.propagate();
	vector<int> new_assumptions;
	if (sat) {
		for (uint32_t i = 0; i < af.args; i++) {
			if (solver.assignment[af.accepted_var[i]-1]) {
				new_assumptions.push_back(af.accepted_var[i]);
			} else if (solver.assignment[af.rejected_var[i]-1]) {
				new_assumptions.push_back(-af.accepted_var[i]);
			}
		}
	}
	return new_assumptions;
}

void print_extension(const AF & af, const std::vector<uint32_t> & extension)
{
	cout << "[";
	for (uint32_t i = 0; i < extension.size(); i++) {
		cout << af.int_to_arg[extension[i]];
		if (i != extension.size()-1) cout << ",";
	}
	cout << "]\n";
}