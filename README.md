# The Orchard
Competency-Based Learning Management System.

The Orchard is a competency based lms centered around Challenges. There are no courses. It is built in Django, and uses the D3 visualization framework to display student progress. 

Learning Objectives are the core building block, and they are assigned to Challenges, and also feed the Competencies, which a student must complete in order to finish the program.

The main applications are: Rubrics, CentralDispatch, and Info.

## Rubrics

The main assessment app. It contains the Learning Objective, Criteria, Challenge, Solution, Rubric, and Rubric Line models. 

**Learning Objectives** are created and assigned any number of criteria. The **criteria** are marked as yes, no, and maybe. Learning Objectives are assigned to **Challenges**, which may or may not have multiple sections. Each challenge will have 1 or more **solutions**, which is the method in which a student uploads their work, and an evaluator assesses it, based on the LO's attached to it. 

A **RubricLine** is created for each LearningObjective that is attached to a solution when an evaluator reviews a student solution. These contain the feedback, user who created them, and the user solution instance they are attached. 

A **Rubric** is created as well, but is attached to the solution, not individual learning objectives. It contains general feedback.

Challenges act as a content delivery model for students as well. They may be **MegaChallenges**, which is a wrapper for a multi-part challenge, or standalone. Each challenge is made up of any number of **Learning Experiences**, which serve as a rich text format page containing the content that a coach or learning designer wants a student to review. At the end of a challenge there will usually be 1 or more aforementioned **solutions**, but they are not required. 

The Challenge navigation is generated dynamically based on the learning experiences contained within. It is paginated, 1 learning experience equals 1 page.


## CentralDispatch

THe tracking and notification application.


## Info

The basic information page system, mainly used for synchronous time with students (in person or virtually). It also contains the experimental features of the Orchard, including the new program design.
