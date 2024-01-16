-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT count(id) FROM assignments where grade='A' AND teacher_id=(SELECT teacher_id FROM assignments where state='GRADED' GROUP BY teacher_id ORDER BY count(*) DESC LIMIT 1);
