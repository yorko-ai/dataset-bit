-- Drop existing tables if they exist
DROP TABLE IF EXISTS files;
DROP TABLE IF EXISTS text_segments;
DROP TABLE IF EXISTS qa_pairs;
DROP TABLE IF EXISTS segments;
DROP TABLE IF EXISTS settings;

-- files table
CREATE TABLE files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT '待处理'
                );


-- text_segments table
CREATE TABLE text_segments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    segment_index INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (file_id) REFERENCES files (id)
                );


-- qa_pairs table
CREATE TABLE qa_pairs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    segment_id INTEGER NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    file_id INTEGER,
                    score INTEGER,
                    FOREIGN KEY (segment_id) REFERENCES text_segments (id)
                );


-- segments table
CREATE TABLE segments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id INTEGER,
                content TEXT NOT NULL,
                segment_index INTEGER NOT NULL,
                created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (file_id) REFERENCES files (id)
            );


-- settings table
CREATE TABLE settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_base TEXT,
            api_key TEXT,
            model_name TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            language TEXT DEFAULT 'zh',
            theme TEXT DEFAULT 'light',
            score_api_url TEXT,
            score_api_key TEXT,
            score_model_name TEXT
        );

-- Create indexes

-- Insert test data

-- files table test data
INSERT OR IGNORE INTO files (filename, file_path, file_size, file_type, status, created_at) 
VALUES 
    ('test_file_1.docx', './uploads/test_file_1.docx', 5740, 'docx', 'done', '2025-05-04 18:00:57'),
    ('test_file_2.md', './uploads/test_file_2.md', 3090, 'md', 'pending', '2025-05-03 18:00:57'),
    ('test_file_3.md', './uploads/test_file_3.md', 5837, 'md', 'pending', '2025-05-02 18:00:57'),
    ('test_file_4.pdf', './uploads/test_file_4.pdf', 5776, 'pdf', 'done', '2025-05-01 18:00:57'),
    ('test_file_5.txt', './uploads/test_file_5.txt', 2194, 'txt', 'pending', '2025-04-30 18:00:57');

-- qa_pairs table test data
INSERT OR IGNORE INTO qa_pairs (segment_id,question,answer,score) VALUES (1,'What is the main content of chunk 1?','This is the answer for chunk 1, question 1...',5),(2,'What is the main content of chunk 2?','This is the answer for chunk 2, question 1...',4),(2,'What is the main content of chunk 2?','This is the answer for chunk 2, question 2...',3),(2,'What is the main content of chunk 2?','This is the answer for chunk 2, question 3...',2),(3,'What is the main content of chunk 3?','This is the answer for chunk 3, question 1...',1),(4,'What is the main content of chunk 4?','This is the answer for chunk 4, question 1...',5),(4,'What is the main content of chunk 4?','This is the answer for chunk 4, question 2...',4),(4,'What is the main content of chunk 4?','This is the answer for chunk 4, question 3...',3),(5,'What is the main content of chunk 5?','This is the answer for chunk 5, question 1...',2),(5,'What is the main content of chunk 5?','This is the answer for chunk 5, question 2...',1);

-- settings table test data
INSERT INTO settings (api_base, api_key, model_name, language, theme, score_api_url, score_api_key, score_model_name) VALUES ('https://api.openai.com/v1', 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'gpt-3.5-turbo', 'en', 'light', 'https://api.openai.com/v1', 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'gpt-3.5-turbo');

-- Create triggers
