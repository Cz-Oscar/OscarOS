INSERT INTO tasks (title, priority)
VALUES
    ('Isc na silownie', 1),
    ('Posprzątać kuchnię', 2),
    ('Zrobić zakupy', 3);

select id, title, priority
from tasks
where completed = FALSE
order by priority ASC;