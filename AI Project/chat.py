import re
import nltk
from autocorrect import Speller
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.chat.util import Chat, reflections
from language_tool_python import LanguageTool

"""nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')"""



college_detail_dict = {
"Principle" : """<body>
    <h1>Dr. K. Prakasan</h1>
</body>""" ,
"About Collage" : """<body>
    <h1>PSG College of Technology</h1>
    <p>PSG College of Technology, founded in 1951, is a leading government-aided institution affiliated with Anna University. Accredited and ISO certified, it boasts 15 engineering departments, renowned faculty, and strong industry ties. With 8518 students, it offers diverse programs, conducts conferences, and fosters research, producing distinguished alumni in various fields. Supported by advanced centers and collaborations, PSG Tech is recognized nationally and internationally for its contributions to technical education and innovation.</p>
    </body>""",   
"About Department" : """<body>
    <h1>Department of Applied Mathematics and Computational Sciences</h1>
    <p>The Department of Applied Mathematics and Computational Sciences comprises of dedicated faculty members who are undoubtedly the assets worthy of mention. The department is known for its discipline and for the importance it gives to the overall development of students in grooming them towards becoming good software professionals, research scientists, and data analysts. The department has its own library with the latest books, national and international journals, and magazines. The computer center is well-equipped with the most recent hardware and software. The department has a vibrant research culture to keep in touch with ever-growing technologies. The faculty members participate regularly in refresher courses and symposia conducted by top-notch Universities, Research Institutions, and Professional Bodies like Association for Computing Machinery, IEEE. The department organizes technical symposia at national and international levels at regular intervals. Apart from stressing consistent and good academic performance, the department encourages participation in co-curricular and extracurricular activities to bring out the latent talents in its students. The students are provided with ample opportunities to improve their organizational skills and group dynamics.</p>
</body>""",
"Former Hod Name" : """<body>
    <h1>Dr. Nadarajan R</h1>
</body>""" ,
"Course Coordinator" : """
<p>Course Coordinator:</p>
<ul>
    <li>MSc Software System: Dr. Periakaruppan R M</li>
    <li>MSc Theoretical Computer Science: Dr. Poonthalir G</li>
    <li>MSc Data Science: Dr. Senthil Kumar M</li>
    <li>MSc Cyber Security: Dr. Shina Sheen</li>
</ul>
""",
"HOD Name" :"""<body>
    <h1>Dr. Shina Sheen</h1>
</body>""" ,
"About HOD" : """<body>
    <h1>Dr. Shina Sheen</h1>
    <h2>Position:</h2>
    <p>Professor and Head, Department of Applied Mathematics and Computational Sciences, PSG College of Technology, Coimbatore, India</p>
    <h2>Education:</h2>
    <p>PhD from Anna University</p>
    <h2>Programme Head:</h2>
    <p>MSc Cyber Security</p>
    <h2>Certifications:</h2>
    <ul>
        <li>SANS GCIA (Intrusion detection in depth)</li>
        <li>Attended live training for GCIH certification programme of SANS (Hacker tools and techniques)</li>
    </ul>
    <h2>Projects Funded by Department of Science and Technology, Government of India:</h2>
    <ol>
        <li>Proactive detection of Ransomware</li>
        <li>Infrastructure development for setting up a Centre for Cybersecurity Research and Education</li>
    </ol>
    <h2>Professional Interests:</h2>
    <p>Computer Security, Data Mining, Proactive Ransomware Detection</p>
    <h2>Memberships:</h2>
    <ul>
        <li>ACM</li>
        <li>Cryptology Research Society of India</li>
        <li>Computer Society of India</li>
    </ul>
</body>""",
      "Founder" : """<body>
    <h1>PSG Family</h1>
    <ul>
        <li>P S GOVINDASWAMY NAIDU (PSG)</li>
        <li>PSG VENKATASWAMY NAIDU</li>
        <li>PSG RANGASWAMY NAIDU</li>
        <li>PSG GANGA NAIDU</li>
        <li>PSG NARAYANASWAMY NAIDU</li>
    </ul>
</body>""",
      "Course" : """<body>
    <h1>Courses offered by our Department</h1>
    <ul>
        <li>MSc Cyber Security</li>
        <li>MSc Data Science</li>
        <li>MSc Software System</li>
        <li>MSc Theoretical Computer Science</li>
    </ul>
</body>
""",
      "location" : """
<body>
    <h1>PSG College of Technology Address</h1>
    <p>PSG College of Technology is located at:</p>
    <p>Avinashi Rd, Peelamedu,<br>Coimbatore, Tamil Nadu 641004</p>
</body>
""",
      "contact" : """
<p>You can contact PSG College of Technology at +91 422 2572177 or via email at <a href="mailto:principal@psgtech.ac.in">principal@psgtech.ac.in</a>.</p>
<p>For specific queries and quick service the following offices can be contacted by email:</p>
<ol>
    <li>Fee payment : <a href="mailto:dean.admn@psgtech.ac.in">dean.admn@psgtech.ac.in</a></li>
    <li>Examination Timetable : <a href="mailto:coe@psgtech.ac.in">coe@psgtech.ac.in</a></li>
    <li>Bona fide Certificates : <a href="mailto:academic@psgtech.ac.in">academic@psgtech.ac.in</a>, <a href="mailto:dean.acad@psgtech.ac.in">dean.acad@psgtech.ac.in</a></li>
    <li>Scholarships : <a href="mailto:dsection.admin@psgtech.ac.in">dsection.admin@psgtech.ac.in</a></li>
    <li>Placement : <a href="mailto:placement@psgtech.ac.in">placement@psgtech.ac.in</a></li>
    <li>Hostel : <a href="mailto:warden.gh@psgtech.ac.in">warden.gh@psgtech.ac.in</a> (boys), <a href="mailto:warden.lh@psgtech.ac.in">warden.lh@psgtech.ac.in</a> (girls)</li>
</ol>
""",
      "admission" : """
<p>Application Closing: 24 MAY 2024</p>
<p>Notification of shortlisted candidates: 28 MAY 2024</p>
<p>Entrance test: 6 JUNE 2024</p>
<p>Counselling in the college campus: 6 JUNE (AFTERNONE) - 11 JUNE 2024</p>
<p>Notification of final selected candidates: 13 JUNE 2024</p>
<p>Last date for fee payment: 20 JUNE 2024</p>
<p>Cost of application: 750 INR</p>
<p>For any further queries contact through <a href="mailto:admission.amcs@psgtech.ac.in">admission.amcs@psgtech.ac.in</a></p>
""",
      "placement" : """
<p>PSG College of Technology's Placement Office facilitates campus recruitment for national and multinational organizations. Led by a Dean, Placement & Training, supported by officers and coordinators, it provides state-of-the-art facilities for interviews and discussions. Over 90 reputed companies visit annually, making PSG Tech one of the top fifteen institutes for student placements nationwide.</p>
<p>Head of Placement: Dr. Nadarajan R.</p>
""",
      "website" : """
<p>You can visit the official PSG College of Technology website for more information: <a href="https://www.psgtech.edu/">PSG Tech Official Website</a>.</p>
""",
      "Timing" : """
<p>The college operates from Monday to Friday, with classes usually scheduled between 8:30 AM to 4:30 PM. Classes may extend till 5:10 PM for 3rd and 5th year students.</p>
""",
      "apply" : """
<p>Application can be made only through online by entering all the particulars including marks along with online payment by Net banking/Credit card/Debit card. One application is sufficient for all the four programmes (SS/TCS/DS/CS) and preference of courses can be selected. All dates are subject to change based on HSC examination results.</p>
""",
      "Payment" : """
<p>Payment can be made online using Net banking, Credit card, or Debit card.</p>
""",
      "Eligibility" : """
<p>An excellent academic record in Higher Secondary examination (10+2) with Mathematics and Physics as subjects is required.</p>
<p>Shortlisted candidates based on Math and Physics HSC marks will sit for an entrance exam on 6th June 2024 (Tentative) at the College campus. The exam duration is ONE hour and will consist of Multiple Choice Questions from Mathematics at +2 level, in English and Tamil.</p>
<p>Counselling for shortlisted candidates will begin on 6th June afternoon at the college campus. The purpose is to assess the applicant's spark and commitment for the 5-year integrated Masters programme (M.Sc SS/TCS/DS/CS) at PSG College of Technology.</p>
<p>The counselling schedule will be notified on the notice board and via registered email after the entrance examination. However, the call for counselling does not guarantee admission.</p>
""",
      "fee" : """
<p>Regarding fee structure or details, I don't have any information. Please contact the college through <a href="mailto:dean.admn@psgtech.ac.in">dean.admn@psgtech.ac.in</a>.</p>
""",
      "Hostel" : """
<p>The Hostel is managed by the Hostel Residents Council consisting of Patron, Chief Warden, Wardens, Manager, Deputy Wardens, Resident Tutors, and Student Representatives.</p>
<p>A student admitted to the institution is not automatically eligible to become a member of the hostel.</p>
<p>Application for admission to the Hostel must be made in the prescribed form. Admissions are made subject to the approval of the Warden.</p>
<p>Before admission, each student has to pay Admission fee, Caution Deposit, Establishment Charges, and Mess Deposit advance which may be revised from time to time. In addition to this, the residents shall share the electricity charge, water charge, and salary paid to the hostel staff.</p>
<p>Every student, before being admitted to the Hostel, shall give an undertaking in writing, endorsed by the parents, that he/she will abide by the Rules and Regulations of the Hostel.</p>
<p>Students admitted to the hostel shall be full boarders of the hostel.</p>
<p>While every effort will be made to accommodate all the aspirants in the Hostel, the following categories of students will not be provided accommodation:</p>
<ol>
    <li>Those who have not cleared mess deposit advance dues of the previous academic year.</li>
    <li>Those who have not paid, Establishment charges and mess Deposit advance in full.</li>
    <li>Those who are possessing powered vehicles.</li>
    <li>Those who were punished for violating hostel rules in previous years.</li>
    <li>Those who have arrears in five subjects or more.</li>
</ol>
""",
        "Mess timing" : """
<p>Morning Tea time: 6:30 am to 7:00 am</p>
<p>Breakfast: 6:30 am to 8:15 am</p>
<p>Lunch: 11:30 am to 1:15 pm</p>
<p>Evening Tea Time: 3:00 pm to 5:30 pm</p>
<p>Dinner: 7:00 pm to 9:00 pm</p>
""",
        "Leave hostel" : """
<p>Residents are permitted to go home/local guardian's place on the 1st and 3rd weekend of every month. In case of important work, residents shall be permitted to go home/local guardian's place after a permission letter is received from the residents' parents through post/courier. The permission letter should be addressed to the warden and received three days in advance of the departure of the residents. In case of urgent work, residents shall go home after obtaining permission from the Warden/Dy. Warden/Resident Tutors.</p>
<p>Residents should register their attendance in the register kept at Avinashi Road main gate whenever they cross the gate.</p>
<p>College ID card is used for the biometric attendance system. In case of missing/lost card, a duplicate card may be provided based on the request and charged (as per norms) in the academic section within a day.</p>
<p><strong>FOR LADIES HOSTEL:</strong></p>
<p>At the time of admission to the hostel, parents are requested to give details (Both father and mother) of their phone/mobile numbers in the hostel application form without fail. They are also informed to make phone calls to the hostel only from their phone/mobile numbers given at the time of admission for all communications. A caller ID system is maintained to ensure that there is no misuse by the residents.</p>
<p>Change of parent's phone numbers should be informed to the hostel office by the parents through the request letter sent from their residential address and phone call from any one of their contact numbers given at the time of admission. In case of any discrepancy, parents should come in person to the hostel.</p>
""",
        "Mess detail" : """
<p>Mess charges will be based on a dividing system.</p>
<p>Residents or their guests shall not enter the kitchen without permission.</p>
<p>Residents shall have their food only in the respective messes allotted to them and they must adhere to the prescribed timings of the mess. Fine will be levied against those who waste food.</p>
<p>Whenever a resident is away from the hostel on valid reason for a period exceeding seven days, reduction in mess charges will be given only for the number of days minus two days (n-2), provided an application for reduction is made in the prescribed form well in advance.</p>
<p>If residents of a particular class leave the hostel for Industrial visits for three days and more, they will be provided mess reduction.</p>
<p>It is not possible to provide mess reduction if a resident has not applied mess reduction in advance. Those who leave hostel in case of emergency should inform their absence by themselves or parents through phone to hostel information service so that mess supervisor will apply mess reduction to the sick residents. After the arrival, copy of medical certificate and college leave application form (signed by class tutor) should be submitted to hostel office.</p>
<p>Residents should obtain tokens for Chicken, Mutton, Chilli Gobi, Omelet, Egg, and Mushroom fry.</p>
<p>Residents should register at their respective mess one day in advance to obtain the above items. Tokens should be used for the reservation day only. Later, the tokens will not be accepted.</p>
<p>Establishment charge shall be paid through Challan of Central Bank of India, Peelamedu (Challan is available at the hostel office), or through Demand Draft, which should be drawn only in favor of PSG Tech Hostel, payable at Coimbatore. In no case, payment by Cash or Cheque will be accepted.</p>
<p>Those who are interested to use North Indian mess shall obtain the North Indian mess card from mess supervisors between 25th to 27th of the preceding month.</p>
<p>Room will not be allotted to those who have not paid the Establishment Charge and mess deposit advance.</p>
<p>Residents shall vacate the hostel whenever they are interested to do so and the establishments charges, once paid will not be refunded.</p>
<p>Since room allotment is done online, Computer will not allot rooms to those who have not paid the establishment charge and mess deposit advance within the specified date.</p>
<p>Students shall view their allotted rooms on our college website http://www.studzone.psgtech.edu/ one day prior to the reopening of the College.</p>
<p>Residents should not bring food from outside.</p>
""",
      "syllabus" : """
<p>Do you want course wise syllabus? If yes, give me the course name:</p>
<ol>
    <li>Cyber Security</li>
    <li>Data Science</li>
    <li>Software System</li>
    <li>Theoretical Computer Science</li>
</ol>
<p>If no, you can continue with other queries.</p>""",
"application" : """
<p>You can find the application form on the PSG College of Technology website:</p>
<p><a href="https://www.psgtech.edu/B.ScMScAdmission2024/">Application Form</a></p>
"""}

cs_dict = {"syllabus cs": """
    <body>
    <h1>Syllabus</h1>
    <h2>Semester 1</h2>
    <ul>
        <li>Calculus and Its Applications</li>
        <li>English for Professional Skills</li>
        <li>Applied Physics</li>
        <li>Digital Electronics</li>
        <li>Problem Solving and C Programming</li>
        <li>Mathematical Foundations Lab</li>
        <li>C Programming Lab</li>
        <li>Applied Physics and Digital Electronics Lab</li>
        <li>Personality And Character Development</li>
    </ul>
    <h2>Semester 2</h2>
    <ul>
        <li>Discrete Structures</li>
        <li>Linear Algebra</li>
        <li>Data Structures and Algorithms</li>
        <li>Object Oriented Programming</li>
        <li>Computer Organization</li>
        <li>Data Structures Lab</li>
        <li>Object Computing Lab</li>
        <li>Python Programming Lab</li>
        <li>Personality And Character Development</li>
    </ul>
    <h2>Semester 3</h2>
    <ul>
        <li>Probability, Stochastic Processes and Statistics</li>
        <li>Linear Algebra</li>
        <li>Microcontrollers And Embedded Systems</li>
        <li>Database Management System</li>
        <li>Design And Analysis Of Algorithms</li>
        <li>Embedded Systems Lab</li>
        <li>Design And Analysis Of Algorithms Lab</li>
        <li>RDBMS Lab</li>
    </ul>
    <h2>Semester 4</h2>
    <ul>
        <li>Optimization Techniques</li>
        <li>Computer Networks</li>
        <li>Cryptography</li>
        <li>Operating Systems</li>
        <li>Hardware Security</li>
        <li>Computer Networks Lab</li>
        <li>Java Programming Lab</li>
        <li>Operating Systems Lab</li>
    </ul>
    <h2>Semester 5</h2>
    <ul>
        <li>Network Security</li>
        <li>Cryptanalysis</li>
        <li>Machine Learning</li>
        <li>Software Security and Exploitation</li>
        <li>Professional Elective I</li>
        <li>Software Security and Exploitation Lab</li>
        <li>Machine Learning Lab</li>
        <li>Ethical Hacking & Malware Analysis Lab</li>
    </ul>
    <h2>Semester 6</h2>
    <ul>
        <li>Cloud Security</li>
        <li>Principles Of Compiler Design</li>
        <li>Data Mining</li>
        <li>Secure Coding</li>
        <li>Professional Elective II</li>
        <li>Cloud Security Lab</li>
        <li>Data Mining And Visualization Lab</li>
        <li>Web Engineering Lab</li>
    </ul>
    <h2>Semester 7</h2>
    <ul>
        <li>Project Work I - Duration of 6 months</li>
    </ul>
    <h2>Semester 8</h2>
    <ul>
        <li>Digital Image Processing and Computer Vision</li>
        <li>Computer Forensics</li>
        <li>Data Privacy</li>
        <li>Professional Elective III</li>
        <li>Open Elective I</li>
        <li>Digital Image Processing and Vision Lab</li>
        <li>Computer Forensics Lab</li>
        <li>Security Capstone Lab</li>
    </ul>
    <h2>Semester 9</h2>
    <ul>
        <li>Threat Hunting</li>
        <li>Blockchain Technology</li>
        <li>Mobile Security</li>
        <li>Professional Elective IV</li>
        <li>Open Elective II</li>
        <li>Threat Hunting Lab</li>
        <li>Mobile Security Lab</li>
        <li>Memory Forensics Lab</li>
    </ul>
    <h2>Semester 10</h2>
    <ul>
        <li>Project Work II - Duration of 6 months</li>
    </ul>
</body>"""}

ds_dict = {"syllabus ds": """
       <body>
    <h1>Syllabus</h1>
    <h2>Semester 1</h2>
    <ul>
        <li>Calculus And Its Applications</li>
        <li>Basics Of Computational Biology</li>
        <li>Digital Electronics</li>
        <li>Problem Solving & C Programming</li>
        <li>English For Professional Skills</li>
        <li>Mathematical Foundations Lab</li>
        <li>C Programming Lab</li>
        <li>Digital Electronics Lab</li>
        <li>Personality And Character Development</li>
    </ul>
    <h2>Semester 2</h2>
    <ul>
        <li>Discrete Structures</li>
        <li>Abstract Algebra</li>
        <li>Data Structures and Algorithms</li>
        <li>Object Oriented Programming</li>
        <li>Theory Of Probability</li>
        <li>Object Computing Lab</li>
        <li>Data Structures Lab</li>
        <li>Python Programming Lab</li>
        <li>Personality And Character Development</li>
    </ul>
    <h2>Semester 3</h2>
    <ul>
        <li>Applied Statistics</li>
        <li>Linear Algebra</li>
        <li>Graph Theory</li>
        <li>Advanced Data Structures</li>
        <li>Computer Organization And Assembly Language Programming</li>
        <li>Applied Statistics And R Programming Lab</li>
        <li>Advanced Data Structures Lab</li>
        <li>Scientific Computing Lab</li>
    </ul>
    <h2>Semester 4</h2>
    <ul>
        <li>Optimization Techniques</li>
        <li>Database Management System</li>
        <li>Predictive Analytics</li>
        <li>Operating Systems</li>
        <li>Transforms And Its Applications</li>
        <li>Data Analytics & Visualisation Lab</li>
        <li>RDBMS Lab</li>
        <li>Operating Systems Lab</li>
    </ul>
    <h2>Semester 5</h2>
    <ul>
        <li>Design And Analysis Of Algorithms</li>
        <li>Stochastic Models</li>
        <li>Computer Networks</li>
        <li>Machine Learning</li>
        <li>Professional Elective-I</li>
        <li>Design And Analysis Of Algorithms Lab</li>
        <li>Machine Learning Lab</li>
        <li>Java Programming Lab</li>
    </ul>
    <h2>Semester 6</h2>
    <ul>
        <li>Cloud Computing</li>
        <li>Deep Learning</li>
        <li>Big Data &Modern Database Systems</li>
        <li>Artificial Intelligence</li>
        <li>Professional Elective II</li>
        <li>Cloud Computing Lab</li>
        <li>Big Data & Modern Database Systems Lab</li>
        <li>Deep Learning Lab</li>
    </ul>
    <h2>Semester 7</h2>
    <ul>
        <li>Project Work I - Duration of 6 months</li>
    </ul>
    <h2>Semester 8</h2>
    <ul>
        <li>Reinforcement Learning</li>
        <li>Natural Language Processing</li>
        <li>Deployable Aspects of Machine Learning</li>
        <li>Professional Elective-III</li>
        <li>Open Elective-I</li>
        <li>Reinforcement Learning Lab</li>
        <li>Deployable Aspects of Machine Learning Lab</li>
        <li>Capstone Project</li>
    </ul>
    <h2>Semester 9</h2>
    <ul>
        <li>Data Privacy And Security</li>
        <li>Data Mining</li>
        <li>Information Retrieval</li>
        <li>Professional Elective IV (Self Study)</li>
        <li>Open Elective-II</li>
        <li>Information Retrieval Lab</li>
        <li>Data Privacy And Security Lab</li>
        <li>Data Mining Lab</li>
    </ul>
    <h2>Semester 10</h2>
    <ul>
        <li>Project Work II - Duration of 6 months</li>
    </ul>
</body>"""}

tcs_dict = {"syllabus tcs": """
       <body>
    <h1>Syllabus</h1>
    <h2>Semester 1</h2>
    <ul>
        <li>Calculus And Its Applications</li>
        <li>Basics Of Computational Biology</li>
        <li>Digital Electronics</li>
        <li>Problem Solving & C Programming</li>
        <li>English For Professional Skills</li>
        <li>Mathematical Foundations Lab</li>
        <li>C Programming Lab</li>
        <li>Digital Electronics Lab</li>
        <li>Personality And Character Development</li>
    </ul>
    <h2>Semester 2</h2>
    <ul>
        <li>Discrete Structures</li>
        <li>Abstract Algebra</li>
        <li>Data Structures and Algorithms</li>
        <li>Object Oriented Programming</li>
        <li>Theory Of Probability</li>
        <li>Object Computing Lab</li>
        <li>Data Structures Lab</li>
        <li>Python Programming Lab</li>
        <li>Personality And Character Development</li>
    </ul>
    <h2>Semester 3</h2>
    <ul>
        <li>Probability And Statistics</li>
        <li>Linear Algebra</li>
        <li>Graph Theory</li>
        <li>Advanced Data Structures</li>
        <li>Computer Organization And Assembly Language Programming</li>
        <li>Statistical Computing And R Programming Lab</li>
        <li>Advanced Data Structures Lab</li>
        <li>Scientific Computing Lab</li>
    </ul>
    <h2>Semester 4</h2>
    <ul>
        <li>Stochastic Processes</li>
        <li>Computer Networks</li>
        <li>Optimization Techniques</li>
        <li>Operating Systems</li>
        <li>Database Management System</li>
        <li>Computer Networks Lab</li>
        <li>Operating Systems Lab</li>
        <li>RDBMS Lab</li>
    </ul>
    <h2>Semester 5</h2>
    <ul>
        <li>Theory Of Computing</li>
        <li>Computational Number Theory And Cryptography</li>
        <li>Machine Learning</li>
        <li>Design And Analysis Of Algorithms</li>
        <li>Professional Elective - I</li>
        <li>Machine Learning Lab</li>
        <li>Design And Analysis Of Algorithms Lab</li>
        <li>Java Programming Lab</li>
    </ul>
    <h2>Semester 6</h2>
    <ul>
        <li>Cloud Computing</li>
        <li>Artificial Intelligence</li>
        <li>Software Engineering</li>
        <li>Principles Of Compiler Design</li>
        <li>Professional Elective II</li>
        <li>Cloud Computing Lab</li>
        <li>Compiler Design Lab</li>
        <li>Software Patterns Lab</li>
    </ul>
    <h2>Semester 7</h2>
    <ul>
        <li>Project Work I - Duration of 6 months</li>
    </ul>
    <h2>Semester 8</h2>
    <ul>
        <li>Game Theory</li>
        <li>Advanced Algorithms</li>
        <li>Data Mining</li>
        <li>Professional Elective III</li>
        <li>Open Elective I</li>
        <li>Functional Programming Lab</li>
        <li>Data Mining and Visualization Lab</li>
        <li>Research Specialization Lab</li>
    </ul>
    <h2>Semester 9</h2>
    <ul>
        <li>Security In Computing</li>
        <li>Digital Image Processing and Computer Vision</li>
        <li>Information Retrieval</li>
        <li>Professional Elective IV</li>
        <li>Open Elective II</li>
        <li>Security In Computing Lab</li>
        <li>Digital Image Processing and Computer Vision Lab</li>
        <li>Information Retrieval Lab</li>
    </ul>
    <h2>Semester 10</h2>
    <ul>
        <li>Project Work II - Duration of 6 months</li>
    </ul>
</body>"""}

ss_dict = {"syllabus ss": """
       <body>
    <h1>Syllabus</h1>
    <h2>Semester 1</h2>
    <ul>
        <li>Calculus and Its Applications</li>
        <li>English for Professional Skills</li>
        <li>Applied Physics</li>
        <li>Digital Electronics</li>
        <li>Problem Solving and C Programming</li>
        <li>Mathematical Foundations Lab</li>
        <li>C Programming Lab</li>
        <li>Applied Physics and Digital Electronics Lab</li>
        <li>Personality And Character Development</li>
    </ul>
    <h2>Semester 2</h2>
    <ul>
        <li>Discrete Structures</li>
        <li>Linear Algebra</li>
        <li>Data Structures and Algorithms</li>
        <li>Object Oriented Programming</li>
        <li>Computer Organization</li>
        <li>Data Structures Lab</li>
        <li>Object Computing Lab</li>
        <li>Python Programming Lab</li>
        <li>Personality And Character Development</li>
    </ul>
    <h2>Semester 3</h2>
    <ul>
        <li>Probability, Stochastic Processes and Statistics</li>
        <li>Database Management System</li>
        <li>Transform Techniques</li>
        <li>Design and Analysis of Algorithms</li>
        <li>Microprocessor and Embedded Systems</li>
        <li>Design and Analysis of Algorithms Lab</li>
        <li>Embedded Systems Lab</li>
        <li>RDBMS Lab</li>
    </ul>
        <h2>Semester 4</h2>
    <ul>
        <li>Accounting and Financial Management</li>
        <li>Computer Networks</li>
        <li>Operations Research</li>
        <li>Operating Systems</li>
        <li>Software Engineering Techniques</li>
        <li>Computer Networks Lab</li>
        <li>Unix System Prograaming Lab</li>
        <li>Web Development Lab</li>
    </ul>
    <h2>Semester 5</h2>
    <ul>
        <li>Big Data and Modern Databases</li>
        <li>Java Programming</li>
        <li>Machine Learning</li>
        <li>Theory Of Computing</li>
        <li>Professional Elective I</li>
        <li>Big Data and Modern Databases Lab</li>
        <li>Java Programming Lab</li>
        <li>Machine Learning Lab</li>
    </ul>
    <h2>Semester 6</h2>
    <ul>
        <li>Cloud Computing</li>
        <li>Artificial Intelligence</li>
        <li>Distributed Computing</li>
        <li>Software Patterns</li>
        <li>Professional Elective II</li>
        <li>Cloud Computing Lab</li>
        <li>Artificial Intelligence Lab</li>
        <li>Mobile Application Development Lab</li>
    </ul>
        <h2>Semester 7</h2>
    <ul>
        <li>Project Work I - Duration of 6 months</li>
    </ul>
    <h2>Semester 8</h2>
    <ul>
        <li>Principles Of Compiler Design</li>
        <li>Data Mining</li>
        <li>Software Project Management</li>
        <li>Professional Elective III</li>
        <li>Open Elective I</li>
        <li>Compiler Design Lab</li>
        <li>Data Mining and Visualization Lab</li>
        <li>Capstone Project Lab</li>
    </ul>
    <h2>Semester 9</h2>
    <ul>
        <li>Digital Image Processing and Computer Vision</li>
        <li>Information Retrieval</li>
        <li>Deep Learning</li>
        <li>Professional Elective IV</li>
        <li>Open Elective II</li>
        <li>Digital Image Processing and Computer Vision Lab</li>
        <li>Information Retrieval Lab</li>
        <li>Deep Learning Lab</li>
    </ul>
    <h2>Semester 10</h2>
    <ul>
        <li>Project Work II - Duration of 6 months</li>
    </ul>
    </body>"""}

tool = LanguageTool('en-US')
memory = []

def spell_check(query):
    matches = tool.check(query)
    corrected_query = tool.correct(query)
    return corrected_query

def preprocess_text(text):
    
    text = spell_check(text)
    # Convert text to lowercase
    text = text.lower()
    
    # Remove special characters, punctuation, and digits using regex
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    return text


def create_chatbot():
    # Define reflections to allow for more human-like conversation
    reflections = {
        "i am": "you are",
        "i was": "you were",
        "i": "you",
        "i'm": "you are",
        "i'd": "you would",
        "i've": "you have",
        "i'll": "you will",
        "my": "your",
        "you are": "I am",
        "you were": "I was",
        "your": "my",
        "yours": "mine",
        "you": "me",
        "me": "you",
    }

    # Define responses for hostel details, college webpage link, location, and timings
    hostel_response = "PSG College of Technology provides separate hostel facilities for both boys and girls. The hostels are well-equipped with all necessary amenities and are supervised by experienced wardens."

    # Define pattern-response pairs for the chatbot
    patterns = [
    (r"(hi|hello|hey)", ["Hello!", "Hi there!", "Hey!"]),
    (r"(good\s*morning)", ["Good morning! How can I assist you today?"]),
    (r"(good\s*afternoon)", ["Good afternoon! How can I assist you today?"]),
    (r"(good\s*evening)", ["Good evening! How can I assist you today?"]),
    (r"(.*)(department)(.*)",[college_detail_dict["About Department"]]),
    (r"(.*)(principle)(.*)",[college_detail_dict["Principle"]]),
    (r"(.*)(course coordinator)(.*)",[college_detail_dict["Course Coordinator"]]),
    (r"(.*)(courses|course)(.*)", [college_detail_dict["Course"]]),
    (r"(.*)(admission)(.*)", [college_detail_dict["admission"]]),
    (r"(.*)(founder)(.*)", [college_detail_dict["Founder"]]),
    (r"(.*)(contact)(.*)", [college_detail_dict["contact"]]),
    (r"(.*)(placement|career)(.*)", [college_detail_dict["placement"]]),
    (r"(.*)(facility|facilities)(.*)", ["PSG College of Technology provides state-of-the-art facilities including well-equipped laboratories, extensive libraries, sports facilities, hostels, and a vibrant student community to support students' academic and extracurricular activities."]),
    (r"(.*)(faculty|professor|staff)(.*)", ["PSG College of Technology has a highly qualified and experienced faculty team consisting of professors, associate professors, and assistant professors who are dedicated to providing quality education and mentorship to students."]),
    (r".*(?:about).*.*(?:staff).*", ["I don't have any personal information about the Staffs"]),
    (r"(.*)(fees|fee)(.*)", [college_detail_dict["fee"]]),
    (r"(.*)(pay|payment)(.*)", [college_detail_dict["Payment"]]),
    (r".*(?=.*syllabus)(?=.*cyber\s*security).*", [cs_dict["syllabus cs"]]),
    (r".*(?=.*syllabus)(?=.*data\s*science).*", [ds_dict["syllabus ds"]]),
    (r".*(?=.*syllabus)(?=.*software\s*system).*", [ss_dict["syllabus ss"]]),
    (r".*(?=.*syllabus)(?=.*theoretical\s*computer\s*science).*", [tcs_dict["syllabus tcs"]]),
    (r"(.*)(syllabus|curriculum)(.*)", [college_detail_dict["syllabus"]]),
    (r"(.*)(help|assist)(.*)", ["How can I assist you today?", "What can I help you with?", "Feel free to ask me anything."]),
    (r"(.*)(hostel mess|detail hostel mess|hostel mess detail)(.*)", [college_detail_dict["Mess detail"]]),
    (r"(.*)(hostel detail|about hostel|detail hostel|hostel)(.*)", [college_detail_dict["Hostel"]]),
    (r"(.*)(hostel mess timing|mess timing|timing mess|timing hostel mess)(.*)", [college_detail_dict["Mess timing"]]),
    (r".*(?:name).*.*(?:former).*.*(?:hod).*", [college_detail_dict["Former Hod Name"]]),
    (r"(.*)(application|form)(.*)", [college_detail_dict["application"]]),
    (r"(.*)(webpage|website)(.*)", [college_detail_dict["website"]]),
    (r"(.*)(location|where)(.*)", [college_detail_dict["location"]]),
    (r"(.*)(timing|timings)(.*)", [college_detail_dict["Timing"]]),
    (r".*(?:name).*.*(?:hod).*", [college_detail_dict["HOD Name"]]),
    (r"(.*)(hod)(.*)", [college_detail_dict["About HOD"]]),
    (r"(.*)(bye|quit|exit)(.*)", ["Bye! Take care."]),
    (r"(.*)(thank you|thanks)(.*)", ["You're welcome!", "Glad I could help!"]),
    (r"(.*)(college|university|institution)(.*)", [college_detail_dict["About Collage"]]),
    (r"(.*)", ["I'm sorry, I didn't quite catch that. Could you please repeat?", "I'm not sure I understand. Can you provide more details?"]),
    ]

    # Initialize NLTK's Chat class with defined patterns and reflections
    chatbot = Chat(patterns, reflections)
    return chatbot

def run_chatbot(user_input):
    # Start the conversation
    print("Welcome to PSG College of Technology Inquiry Chatbot!")
    print("Feel free to ask any questions about PSG College of Technology. Type 'bye' to exit.")

    
    chatbot = create_chatbot()

    user_input = preprocess_text(user_input)
    
    memory.append(user_input)
    if(len(memory) != 1):
        if("syllabus" in memory[len(memory)-2] and ("cybersecurity" in user_input or  "data science" in user_input or "software system" in user_input or "theoretical computer science" in user_input)): 
            user_input = "syllabus " + user_input
    response = chatbot.respond(user_input)
    print(user_input)
    #print("user_input:",user_input)
    #print("Bot:", response)
    return response

        

