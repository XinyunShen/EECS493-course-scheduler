PRAGMA foreign_keys
= ON;

INSERT INTO users
        (username, fullname, email, filename, password)
VALUES
        ('xinyun', 'Xinyun Shen', 'xinyun@umich.edu',
                'xinyun.jpg',
                'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'
        );

INSERT INTO users
        (username, fullname, email, filename, password)
VALUES
        ('alexzw', 'Alex Wang', 'alexzw@umich.edu',
                'alex.jpg',
                'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'
        );

INSERT INTO users
        (username, fullname, email, filename, password)
VALUES
        ('changjus', 'Justin Chang', 'changjus@umich.edu',
                'changju.jpg',
                'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'
        );

INSERT INTO users
        (username, fullname, email, filename, password)
VALUES
        ('rayku', 'Raymond Ku', 'rayku@umich.edu',
                'raykuu.jpg',
                'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'
        );

INSERT INTO following
        (username1, username2)
VALUES
        ('xinyun', 'alexzw');

INSERT INTO following
        (username1, username2)
VALUES
        ('alexzw', 'xinyun');

INSERT INTO following
        (username1, username2)
VALUES
        ('changjus', 'rayku');

INSERT INTO course
        (courseid, credits, coursename, description, prerequisite)
VALUES
        ('101', 4, 'Thriving in a Digital World', 'From mobile apps to bitmaps, this course explores computational technologies and how they impact society and our everyday lives. Topics include: social networks, creative computing, algorithms, security and digital privacy. Traditional computer programming is not a primary focus. Instead, mobile applications will be created using a novel visual programming environment.', 'none'),
        ('180', 3, 'Exam/Transfer Introductory Computer Programming Credit', 'Credit for college-level introductory programming coursework based on a satisfactory score on an approved exam (e.g., a score of 5 on the AP Computer Science A exam) or on transfer credit for an approved introductory programming course at another college. Indicates preparedness to proceed to EECS 280.', 'none'),
        ('183', 4, 'Elementary Programming Concepts', 'Fundamental concepts and skills of programming in a high-level language. Flow of control: selection, iteration, subprograms. Data structures: strings, arrays, records, lists, tables. Algorithms using selection and iteration (decision making, finding maxima/minima, searching, sorting, simulation, etc.) Good program design, structure and style are emphasized. Testing and debugging. Not intended for Engineering students (who should take ENGR 101), nor for CS majors in LSA who qualify to enter EECS 280.', 'none'),
        ('198', 4, 'Special Topics', 'Topics of current interest selected by the faculty. Lecture, seminar, or laboratory.', 'none'),
        ('200', 2, 'Electrical Engineering Systems Design I', 'Gain a systems engineering perspective of electrical engineering centered around a design competition to address a societally-relevant challenge. Apply electrical engineering concepts in circuits, computing, control, sensors, optics, power, signal processing, and wireless communications to a system such as a robot, and adapt the system to achieve competition objectives within defined engineering constraints.', 'ENGR 100 or ENGR 101 or ENGR 151 or EECS 180 or EECS 280. Preceded or accompanied by: EECS 215 Minimum grade of “C” for advised prerequisites.'),
        ('201', 1, 'Computer Science Pragmatics', 'Essential tools for computer programming:  Shells, environments, scripting, Makefiles, compilers, debugging tools, and version control.', 'EECS 180 or EECS 183 or ENGR 101 or ENGR 151 or preceded or accompanied by (EECS 280 or EECS 281). Minimum grade of “C” required for enforced prerequisites.'),
        ('203', 4, 'Discrete Mathematics', 'Introduction to the mathematical foundations of computer science. Topics covered include: propositional and predicate logic, set theory, function and relations, growth of functions and asymptotic notation, introduction to algorithms, elementary combinatorics and graph theory and discrete probability theory.', '(MATH 115 or 116 or 119 or 120 or 121 or 156 or 175 or 176 or 185 or 186 or 214 or 215 or 216 or 217 or 255 or 256 or 285 or 286 or 295 or 296 or 417 or 419). Minimum grade of C required for enforced prerequisites.'),
        ('215', 4, 'Introduction to Electronic Circuits', 'laws; Ohm’s law; voltage and current sources; Thevenin and Norton equivalent circuits; DC and low frequency active circuits using operational amplifiers, diodes, and transistors; small signal analysis; energy and power. Time- and frequency-domain analysis of RLC circuits. Basic passive and active electronic filters. Laboratory experience with electrical signals and circuits.', '(MATH 116 or 121 or 156) and (ENGR 101 or 151 or EECS 180 or 183 or preceded or accompanied by EECS 280) and (preceded or accompanied by: PHYSICS 240 or 260); (C or better, No OP/F) Cannot receive credit for both EECS 314 and EECS 215. Minimum grade of C required for enforced prerequisites.'),
        ('216', 4, 'Introduction to Signals and Systems', 'Theory and practice of signals and systems engineering in continuous and discrete time. Continuous-time linear time-invariant systems, impulse response, convolution. Fourier series, Fourier transforms, spectrum, frequency response and filtering. Sampling leading to basic digital signal processing using the discrete-time Fourier and the discrete Fourier transform. Laplace transforms, transfer functions, poles and zeros, stability. Applications of Laplace transform theory to RLC circuit analysis. Introduction to communications, control and signal processing. Weekly recitations and hardware/Matlab software laboratories.', 'EECS 215 or EECS 314 or BIOMEDE 211, preceded or accompanied by MATH 216.'),
        ('230', 4, 'Electromagnetics I', 'Vector calculus. Electrostatics. Magnetostatics. Time-varying fields: Faraday’s Law and displacement current. Maxwell’s equations in differential form. Traveling waves and phasors. Uniform plane waves. Reflection and transmission at normal incidence. Transmission lines. Laboratory segment may include experiments with transmission lines, the use of computer-simulation exercises, and classroom demonstrations.', 'MATH 215, PHYS 240 (or 260), EECS 215');


INSERT INTO coursetime
        (courseid, timeid, starttime, endtime, weekday)
VALUES
        ('101', 1, '9:00', '10:30', 'Monday Wednesday'),
        ('101', 2, '11:00', '12:30', 'Monday Wednesday'),
        ('180', 3, '11:00', '12:30', 'Monday Wednesday'),
        ('180', 4, '12:30', '14:00', 'Monday Wednesday'),
        ('183', 5, '14:15', '15:45', 'Monday Wednesday Friday'),
        ('183', 6, '15:45', '16:45', 'Monday Wednesday Friday'),
        ('198', 7, '10:00', '11:00', 'Tuesday Thursday'),
        ('198', 8, '11:00', '12:00', 'Tuesday Thursday'),
        ('200', 9, '10:30', '12:00', 'Tuesday Thursday'),
        ('200', 10, '12:00', '13:00', 'Tuesday Thursday'),
        ('201', 11, '16:00', '17:30', 'Tuesday'),
        ('201', 12, '17:30', '18:00', 'Thursday'),
        ('203', 13, '08:00', '09:00', 'Friday'),
        ('215', 14, '9:00', '10:00', 'Friday'),
        ('216', 15, '15:45', '16:45', 'Friday'),
        ('230', 16, '13:00', '14:30', 'Friday');

INSERT INTO schedule
        (username, courseid, timeid)
VALUES
        ('xinyun', '101', 1),
        ('xinyun', '180', 3),
        ('xinyun', '183', 5),
        ('alexzw', '198', 8),
        ('alexzw', '200', 10);

INSERT INTO schedule
        (username, courseid, timeid)
VALUES
        ('changjus', '101', 2),
        ('changjus', '180', 4),
        ('changjus', '198', 8),
        ('changjus', '201', 11),
        ('changjus', '203', 13),
        ('rayku', '101', 1),
        ('rayku', '183', 6),
        ('rayku', '200', 9),
        ('rayku', '201', 11),
        ('rayku', '216', 15);
        