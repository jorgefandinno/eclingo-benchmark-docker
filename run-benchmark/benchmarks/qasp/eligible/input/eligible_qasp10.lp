fairGPA(mary).
highGPA(mary).
minority(mary).
fairGPA(mike).
highGPA(mike).
highGPA(nancy).
fairGPA(paul).
minority(paul).
fairGPA(pat).
minority(peter).
highGPA(peter).
fairGPA(sam).
highGPA(sam).
minority(sam).
highGPA(tim).
-highGPA(tom).
-fairGPA(tom).
minority(tom).
-highGPA(van).
-fairGPA(van).
minority(van).
student(pat).
student(van).
student(tom).
student(mike).
student(peter).
student(mary).
student(tim).
student(nancy).
student(paul).
student(sam).
eligible(X) :- highGPA(X), student(X).
eligible(X) :- minority(X), fairGPA(X), student(X).
-eligible(X) :- -fairGPA(X), -highGPA(X), student(X).
interview(X) :- not K$ eligible(X), not K$ -eligible(X), student(X).
