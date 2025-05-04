
-- files table
CREATE TABLE files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                , status TEXT DEFAULT '待处理');


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
                    quality_scores TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, file_id INTEGER,
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
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        , language TEXT DEFAULT 'zh', theme TEXT DEFAULT 'light');

-- Create indexes

-- Insert test data

-- files table test data
INSERT OR IGNORE INTO files (filename,file_path,file_size,file_type,status,upload_time) VALUES ('test_file_1.docx','./uploads/test_file_1.docx',5740,'docx','done','2025-05-04 18:00:57'),('test_file_2.md','./uploads/test_file_2.md',3090,'md','pending','2025-05-03 18:00:57'),('test_file_3.md','./uploads/test_file_3.md',5837,'md','pending','2025-05-02 18:00:57'),('test_file_4.pdf','./uploads/test_file_4.pdf',5776,'pdf','done','2025-05-01 18:00:57'),('test_file_5.txt','./uploads/test_file_5.txt',2194,'txt','pending','2025-04-30 18:00:57');

-- qa_pairs table test data
INSERT OR IGNORE INTO qa_pairs (chunk_id,question,answer) VALUES (1,'What is the main content of chunk 1?','This is the answer for chunk 1, question 1...'),(2,'What is the main content of chunk 2?','This is the answer for chunk 2, question 1...'),(2,'What is the main content of chunk 2?','This is the answer for chunk 2, question 2...'),(2,'What is the main content of chunk 2?','This is the answer for chunk 2, question 3...'),(3,'What is the main content of chunk 3?','This is the answer for chunk 3, question 1...'),(4,'What is the main content of chunk 4?','This is the answer for chunk 4, question 1...'),(4,'What is the main content of chunk 4?','This is the answer for chunk 4, question 2...'),(4,'What is the main content of chunk 4?','This is the answer for chunk 4, question 3...'),(5,'What is the main content of chunk 5?','This is the answer for chunk 5, question 1...'),(5,'What is the main content of chunk 5?','This is the answer for chunk 5, question 2...'),(5,'What is the main content of chunk 5?','This is the answer for chunk 5, question 3...'),(6,'What is the main content of chunk 6?','This is the answer for chunk 6, question 1...'),(6,'What is the main content of chunk 6?','This is the answer for chunk 6, question 2...'),(6,'What is the main content of chunk 6?','This is the answer for chunk 6, question 3...'),(7,'What is the main content of chunk 7?','This is the answer for chunk 7, question 1...'),(7,'What is the main content of chunk 7?','This is the answer for chunk 7, question 2...'),(7,'What is the main content of chunk 7?','This is the answer for chunk 7, question 3...'),(8,'What is the main content of chunk 8?','This is the answer for chunk 8, question 1...'),(8,'What is the main content of chunk 8?','This is the answer for chunk 8, question 2...'),(8,'What is the main content of chunk 8?','This is the answer for chunk 8, question 3...'),(9,'What is the main content of chunk 9?','This is the answer for chunk 9, question 1...'),(9,'What is the main content of chunk 9?','This is the answer for chunk 9, question 2...'),(10,'What is the main content of chunk 10?','This is the answer for chunk 10, question 1...'),(10,'What is the main content of chunk 10?','This is the answer for chunk 10, question 2...'),(11,'What is the main content of chunk 11?','This is the answer for chunk 11, question 1...'),(11,'What is the main content of chunk 11?','This is the answer for chunk 11, question 2...'),(11,'What is the main content of chunk 11?','This is the answer for chunk 11, question 3...'),(12,'What is the main content of chunk 12?','This is the answer for chunk 12, question 1...'),(12,'What is the main content of chunk 12?','This is the answer for chunk 12, question 2...'),(13,'What is the main content of chunk 13?','This is the answer for chunk 13, question 1...'),(13,'What is the main content of chunk 13?','This is the answer for chunk 13, question 2...');

-- settings table test data
INSERT INTO settings (api_base, api_key, model_name, language, theme) VALUES ('https://api.openai.com/v1', 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'gpt-3.5-turbo', 'en', 'light');

-- Create triggers
