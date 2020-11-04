ALTER TABLE authors ADD UNIQUE KEY id (id);
ALTER TABLE books ADD UNIQUE KEY id (id), ADD UNIQUE KEY barcode (barcode);
ALTER TABLE book_types ADD UNIQUE KEY id (id);
ALTER TABLE issues ADD UNIQUE KEY id (id);
ALTER TABLE issue_types ADD UNIQUE KEY id (id);
ALTER TABLE users ADD UNIQUE KEY id (id), ADD UNIQUE KEY vkId (vkId);