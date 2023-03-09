//#include "pch.h"




//NumerOLA3.cpp
//DUe Date: 10/01/20
//Author: Sean Gately
//CSCI 3180
//Derive a newton polynomial given a set of points and compare the polynomial to the function which it is meant to emulate.
//Input: set of x values, set of test values
//output, resulting y values for each the x and test values as well as the difference between the polynomial and function


#include <iostream>
#include <math.h>
#include <vector>
#include <string>
#include <sstream>
#include <iomanip>



using namespace std;

double func(double);

void dividedDifference(vector<double> &x, vector<double> &y);

double polyConstruct(vector<double> yVals, vector<double> xVals, int val);


int main()
{
	vector<double> xVals;
	vector<double> yVals;
	vector<double> testVals;
	string temp;
	cout << "Input some numbers separated by spaces: ";
	getline(cin, temp);
	istringstream dubbles(temp);
	double dubbletemp;
	while (!dubbles.eof()) {
		dubbles >> dubbletemp;
		xVals.push_back(dubbletemp);
	}
	for (vector<double>::iterator ptr = xVals.begin(); ptr < xVals.end(); ptr++) {
		yVals.push_back(func(*ptr));
	}
	dividedDifference(xVals, yVals);
	cout << "Alright, cool. Now Enter a bunch of numbers to be tested: ";
	getline(cin, temp);
	istringstream newDubbles(temp);
	double newDubbleTemp; //I don't like doing this.
	while (!newDubbles.eof()) {
		newDubbles >> newDubbleTemp;
		testVals.push_back(newDubbleTemp);
	}


	cout << "i  |  Xi  |   f(Xi)   |   P(Xi)   |     f(Xi) - P(Xi)   |" << endl << "-----------------------------------------------------------" << endl;
	double fXi;
	double pXi;
	int i = 0;

	for (vector<double>::iterator pit = testVals.begin(); pit < testVals.end(); pit++) {
		cout << i << "     " << *pit << "    " << setprecision(8) << func(*pit) << "    ";
		cout << polyConstruct(yVals, xVals, *pit) << "    " << (func(*pit) - polyConstruct(yVals, xVals, *pit)) << endl;
		i++;
	}
	
	return 0;
}

double func(double x){
	return (1 / (pow(x, 2) + 1));
}
//Here's the plan; two iterators, one for x and one for y. 
//the y iterator will be reset to y.begin() + 1 after each pass.
void dividedDifference(vector<double> &xVals, vector<double> &yVals) {
	vector<double>::iterator xit = xVals.begin();
	vector<double>::iterator yit = yVals.begin();
	int y = 0;
		while ((yit + 1) < yVals.end()) {
			
			vector<double> coolVec;
			for (yit = yVals.begin() + y; (yit + 1) < yVals.end(); yit++) {
				coolVec.push_back(((*(yit + 1) - *yit)) / (*(xit + y + 1) - *xit));
				xit++;
			}
			vector<double>::iterator cit = coolVec.begin();
			//here we assign new values to yvals from the new vector
			for (yit = yVals.begin() + y + 1; yit < yVals.end(); yit++) {
				*yit = *cit;
				cit++;
			}
			cout << "Iteration " << y << endl;
			for (yit = yVals.begin(); yit < yVals.end(); yit++) {
				cout << *yit << endl;
			}
			y++;
			yit = (yVals.begin() + y);
			xit = xVals.begin();
			
		}
	return;
}

double polyConstruct(vector<double> yVals, vector<double> xVals, int val) {
	double result = *yVals.begin();
	int x = 1; //used to process inner loop
	for (vector<double>::iterator yit = yVals.begin() + 1; yit < yVals.end(); yit++) {
		double iterVal = *yit;
		vector<double>::iterator xit = xVals.begin();
		for (int y = 0; y < x; y++) {
			iterVal *= (val - *xit);
			xit++;
		}
		result += iterVal;
		x++;
	}
	return result;
}
