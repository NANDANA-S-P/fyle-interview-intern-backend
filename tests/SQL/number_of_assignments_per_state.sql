-- Write query to get number of assignments for each state
SELECT "DRAFT",count(*) FROM assignments WHERE state='DRAFT' 
UNION
SELECT "GRADED",count(*) FROM assignments WHERE state='GRADED' 
UNION
SELECT "SUBMITTED",count(*) FROM assignments WHERE state='SUBMITTED' 