# schema.sql

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(36) UNIQUE NOT NULL,  -- 客户端生成的UUID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI角色表
CREATE TABLE IF NOT EXISTS ai_roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    system_prompt TEXT NOT NULL,  -- 系统提示词，用于设置AI角色
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 对话表
CREATE TABLE IF NOT EXISTS conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    role_id INT NOT NULL,
    title VARCHAR(255) NOT NULL DEFAULT '新对话',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (role_id) REFERENCES ai_roles(id)
);

-- 消息表
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id INT NOT NULL,
    role ENUM('user', 'assistant') NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

-- 插入默认AI角色
INSERT INTO ai_roles (name, description, system_prompt) VALUES
('通用助手', '一个全能型AI助手，可以回答各类问题。', '你是一个乐于助人的AI助手，擅长回答各种问题。'),
('程序员助手', '帮助你解决编程问题，提供代码示例和建议。', '你是一个编程专家，擅长帮助用户解决各种编程问题，提供清晰的代码示例和技术建议。'),
('学习导师', '帮助你学习各种知识，解答学术问题。', '你是一个耐心的学习导师，擅长解释复杂概念，回答学术问题，并提供学习建议。'),
('心理咨询师', '提供心理支持和建议，帮助你处理情绪和压力。', '你是一个善解人意的心理咨询师，擅长倾听，提供情感支持，帮助用户处理压力和情绪问题。');