# Existing Systems Comparison: DATERA EDU

## 1. Purpose

The proposed system works like this. A teacher uploads course materials, and then the recording of a one-to-one lesson in English, Russian or a mix of both. The system checks the student's answers against the materials and shows which topics the student understood and which ones need more work. It keeps this history for every student and sends separate reports to the teacher, the student and the parent. Kazakh and group lessons are planned for later. Before development starts, it helps to know what already exists, what these products do well and where they stop. This document compares five of them with the proposed system.

## 2. Selection of systems

The selection included products that are actually used in practice, or that are very close to the idea of the project, and that apply AI to recorded lessons or calls. Five systems from three groups were selected (Table 1).

**Table 1 - Systems selected for comparison**

| Group | System | Reason for choosing it |
| :--- | :--- | :--- |
| **AI assistants in video-call tools** | Zoom AI Companion | The most common tool for online lessons. Makes summaries of calls and cloud recordings. |
| | Google Meet (Gemini "Take notes for me") | Second most common tool for online lessons. Writes meeting notes automatically. |
| **AI for tutoring lessons** | Preply Lesson Insights | Closest to the idea of the project. After each one-to-one lesson, an LLM reads the transcript and writes a report. |
| **Speech-based tools for schools** | Microsoft Reading Progress | Free and widely used in schools. Assesses students from their speech. |
| | TeachFX | The best-known product that analyses audio from real classrooms. |

Three other options were considered but not included. Yandex Telemost makes call summaries like Zoom, but the supported languages could not be found in available sources [11]. Kundelik.kz is the school e-diary that most parents in Kazakhstan use; it stores grades and attendance and does not analyse lessons, so it shows how things work today rather than being a competitor. M-Powering Teachers from Stanford gives feedback to teachers on how they talk with students, but it is a research project, not a product [10].

## 3. Criteria

Nine criteria were used. Each one comes from a requirement of the proposed system, so the comparison shows how far each product is from what the project needs (Table 2).

**Table 2 - Comparison criteria**

| No. | Criterion | Why it matters for the project |
| :--- | :--- | :--- |
| C1 | Works with any lesson recording, including lessons in a classroom | Tutors work online and offline and use different platforms. |
| C2 | Separates teacher and student speech | The system must know which answers came from the student. |
| C3 | Assesses what the student knows, topic by topic | This is the main function of the proposed system. |
| C4 | Shows evidence from the recording (time codes, quotes) | Teachers need to check the result before they trust it. |
| C5 | Tracks the progress of each student over time | Learning happens over many lessons, not one. |
| C6 | Has reports for parents | Parents are one of the target user groups. |
| C7 | Gives practice on weak topics after the lesson | A diagnosis is more useful when it leads to practice. |
| C8 | Supports English, Russian and mixed speech; Kazakh later | The first users teach in English and Russian and may switch between them inside one lesson. Kazakh is the next step. |
| C9 | Fits Kazakhstan's personal data rules (data stored in Kazakhstan, consent of parents) | Many students are children, and recordings contain their voices. |

## 4. Comparison table

*Notation: Yes - supported; Partly - supported with limits; No - not supported; N/D - not described in the available sources (this does not prove the feature is missing); N/A - not applicable; Yes\* - planned in the proposed system. Numbers in brackets refer to the list of sources in Section 7.*

**Table 3 - Comparison of existing systems with the proposed system**

| Criterion | Zoom AI Companion | Google Meet (Gemini) | Preply Lesson Insights | MS Reading Progress | TeachFX | Proposed system |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **C1. Works with any recording, incl. offline lessons** | Partly - only meetings held in Zoom [1] | Partly - live Meet calls; file upload not described [3] | No - only lessons inside Preply [5] | No - student reads a given text in Teams [6] | Partly - own app or Zoom integration; file upload not described [8] | Yes* - any audio or video file |
| **C2. Separates teacher and student speech** | N/D | N/D | N/D - the tutor's and the learner's audio seem to be handled separately, but the method is not described [12] | N/A - only the student speaks [6] | Yes - teacher talk vs. student talk [8] | Yes* - teacher can fix labels |
| **C3. Assesses what the student knows, by topic** | No - meeting summary, chapters, next steps [1] | No - notes and action items [4] | Partly - only language skills: grammar, vocabulary, pronunciation [5] | Partly - only reading fluency: accuracy, words per minute [6], [7] | No - looks at the teacher: talk time, questions, wait time [8], [9] | Yes* - mastery index per topic with a colour status, checked against the teacher's materials |
| **C4. Shows evidence from the recording** | Partly - chapters with time stamps, no assessment [1] | N/D | N/D - no quotes or time codes are mentioned [5], [12] | Yes - reading errors marked on the audio [6] | N/D | Yes* - time codes for each score |
| **C5. Tracks student progress over time** | N/D | N/D | Partly - announced as future work [5] | Yes - Insights tab, per student and class [6], [7] | No - reports are about the teacher [8] | Yes* - knowledge map |
| **C6. Reports for parents** | No | No | No - learner and tutor only [5] | N/D - teacher and student only [6] | No - only the teacher sees recordings [8] | Yes* - separate parent report |
| **C7. Practice on weak topics after the lesson** | No | No | Yes - exercises generated from the lesson [5] | Partly - practice on difficult words [7] | No | Yes* (stage 2) - quiz on weak topics; questions can be generated from the teacher's materials |
| **C8. Supports English, Russian and mixed speech; Kazakh later** | Partly - English and Russian yes, Kazakh no [2] | Partly - English yes, Russian and Kazakh no; one language per meeting [3] | Partly - English lessons only [12] | Partly - Russian yes, Kazakh no [6] | N/D | Yes* - English, Russian, mixed; Kazakh later |
| **C9. Fits Kazakhstan data rules (data stored in KZ, parent consent)** | N/D | N/D | Partly - consent step, GDPR, SOC 2; place of storage is not stated [12] | N/D | Partly - US rules (FERPA, COPPA), not KZ [8] | Yes* - servers in KZ, consent step |

## 5. Analysis

All five products solve part of the problem. Zoom and Google Meet are mature and used by millions of people, and their summaries are useful for remembering what a lesson was about. But they describe the conversation, not the student. A summary will say that the lesson covered quadratic equations; it will not say whether the student actually understood them.

Microsoft Reading Progress is interesting because it proves that schools accept assessment based on a student's voice. It counts reading errors, marks them on the recording and keeps a history for each student. It only works when the student reads a given text aloud, though, so it cannot judge understanding in a normal conversation. TeachFX works with real classroom audio and separates teacher and student talk, but it gives feedback to the teacher about their teaching style.

Preply Lesson Insights is the closest product to the proposed system. After a one-to-one lesson, the audio is transcribed and an LLM writes feedback on grammar, vocabulary and speaking, with exercises on top [5], [12]. Its limits matter for this project. Right now it works only for English lessons, and only for lessons held on Preply [12]. It looks at language skills, not at the topics of a school subject. Parents, quotes from the recording and time codes are not mentioned. A tutor or a learning centre in Kazakhstan cannot upload their own lessons to it.

Putting the table together, none of the five products:
1) judges how well a student understood the topics of a lesson, for any subject, using the teacher's own materials as the reference (C3);
2) connects each judgement to a moment in the recording and collects these results into a knowledge map for each student (C4, C5);
3) prepares a report for parents (C6);
4) works with mixed English-Russian speech or with Kazakh: Google Meet notes handle one language per meeting and do not list Russian [3], Preply Lesson Insights works for English only [12], and none of the five lists Kazakh (C8);
5) accepts recordings from any source, including lessons recorded on a phone in a classroom (C1);
6) states that it follows Kazakhstan's personal data rules (C9).

Transcription and summaries already exist. What is missing is the step from "what was said in the lesson" to "what the student understood". The result has to be something a teacher can check and a parent can read, and it has to hold up when a lesson switches between English and Russian.

Kazakh is a later step, after the first version. The literature review comes to the same conclusion from the research side (see its discussion of research gaps).

The weaknesses of the proposed system should also be stated. It will not have the scale, stability or real-time features of Zoom and Google Meet, and it will start without the users and data that Preply has. Its accuracy also still has to be proven in tests with real teachers. For this reason it is positioned as an addition to video-call tools, not a replacement: a tutor can record a lesson in Zoom or Meet and then upload the file to the proposed system. The first version works only with one-to-one lessons, and tests on weak topics come in the second stage.

## 6. Limitations

This comparison is based on public documentation, not on hands-on testing. A product may have features that are not described online, which is why "N/D" is kept separate from "No". AI features also change quickly, so the table reflects the situation on October 2026.

## 7. Sources

1. The New School IT. How to Use AI Companion with Cloud Recordings. https://services.newschool.edu/TDClient/32/Portal/KB/ArticleDet?ID=1389
2. Zoom Support. Supported languages for Zoom AI features. https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0078144
3. Google Meet Help. Take notes for me in Google Meet. https://support.google.com/meet/answer/14754931?hl=en
4. Google. Take notes for me (announcement, 29 June 2026). https://blog.google/products-and-platforms/products/workspace/take-notes-for-me/
5. OpenAI. Preply (customer story about Lesson Insights). https://openai.com/index/preply
6. Microsoft Support. Getting started with Reading Progress in Teams. https://support.microsoft.com/en-US/education/getting-started-with-reading-progress-in-teams
7. FLTMAG. Microsoft's Reading Progress Tool: Harnessing the Potential of L2 Oral Reading Assignments Through Technology. July 2023. https://fltmag.com/microsoft-reading-progress/
8. TeachFX. Frequently Asked Questions. https://www.teachfx.com/faq
9. TeachFX. See classroom conversation patterns. https://teachfx.com/blog/see-classroom-conversation-patterns
10. Demszky D., Liu J. M-Powering Teachers: Natural Language Processing Powered Feedback Improves 1:1 Instruction and Student Outcomes. EdWorkingPaper ai23-759, 2023. https://scale.stanford.edu/publications/m-powering-teachers-natural-language-processing-powered-feedback-improves-11
11. ComNews. Яндекс превратит Телемост в универсальный инструмент для общения. 30 October 2025. https://www.comnews.ru/content/242089/2025-10-30/2025-w44/1010/yandeks-prevratit-telemost-universalnyy-instrument-dlya-obscheniya
12. Preply Help Center. Lesson notes (Lesson Insights). https://help.preply.com/ru/articles/10385861-заметки-об-уроке