CREATE TABLE bites_biteconsumer (
    id SERIAL PRIMARY KEY,
    bite_id INTEGER NOT NULL,
    comments TEXT,
    added TIMESTAMP WITH TIME ZONE NOT NULL
);

INSERT INTO bites_biteconsumer (bite_id, comments, added) VALUES
    (229, 'Nice Bite! Learned (once again) to always proof-read my code.', NOW()),
    (229, 'I have always struggled with loops, so this was very good practice.', NOW()),
    (276, 'It was only difficult because I forgot why we were defining.', NOW()),
    (276, 'Not sure if I am missing something on this one.', NOW()),
    (142, 'Challenging but rewarding!', NOW()),
    (142, 'This could use better explanation.', NOW());
