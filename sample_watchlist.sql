-- Sample Watchlist Data for Anti-Narcotics Force
-- Add known drug traffickers and suspects

USE gtas;

-- First, check what watchlist categories exist
-- SELECT * FROM watchlist_category;

-- Insert sample suspects (matching passengers from your Excel files)
INSERT INTO watchlist (first_name, last_name, dob) VALUES
('ZAHEER', 'ABBAS', '1982-02-01'),
('MUHAMMAD', 'ALI', '1990-01-01'),
('SHAHZAD', 'ABBASI', '1989-09-25'),
('FARAH', 'ABID', '1990-08-08');

-- Add with document numbers for exact matching
INSERT INTO watchlist (first_name, last_name, dob, document_number, document_type) VALUES
('HASSANAIN', 'ABBAS', '2009-03-05', 'WG1017041', 'P'),
('YAWAR', 'ABBAS', '2009-03-10', 'XF1011151', 'P'),
('MUDASSAR', 'ABBAS', '2003-06-01', 'TZ1014501', 'P');

-- Verify watchlist entries
SELECT * FROM watchlist ORDER BY id DESC LIMIT 10;
