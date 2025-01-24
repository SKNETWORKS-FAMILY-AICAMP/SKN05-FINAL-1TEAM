// Input.tsx
import React, { useState } from 'react';
import styles from './Input.module.css';

type InputProps = {
    onSendMessage: (message: string) => void;
};

const Input: React.FC<InputProps> = ({ onSendMessage }) => {
    const [inputValue, setInputValue] = useState('');

    const handleSend = () => {
        if (inputValue.trim()) {
            onSendMessage(inputValue);
            setInputValue('');
        }
    };

    return (
        <div className={styles.inputContainer}>
            <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                className={styles.inputField}
                placeholder="Type your message here..."
            />
            <button onClick={handleSend} className={styles.sendButton}>
                Send
            </button>
        </div>
    );
};

export default Input;

// Message.tsx
import React from 'react';
import styles from './Message.module.css';

type MessageProps = {
    message: string;
    isUserMessage: boolean;
};

const Message: React.FC<MessageProps> = ({ message, isUserMessage }) => {
    return (
        <div className={isUserMessage ? styles.userMessage : styles.botMessage}>
            <div className={styles.messageContent}>
                {message}
            </div>
        </div>
    );
};

export default Message;

// Container.tsx
import React, { useState } from 'react';
import ChatInput from '@/app/components/chat/ChatInput';
import Message from '@/app/components/chat/ChatOutput';
import styles from '@/app/styles/chat.module.css';

const Container: React.FC = () => {
    const [messages, setMessages] = useState<Array<{ text: string; isUser: boolean }>>([]);

    const handleSendMessage = (message: string) => {
        setMessages((prevMessages) => [
            ...prevMessages,
            { text: message, isUser: true },
            { text: `Echo: ${message}`, isUser: false }, // Placeholder for bot response
        ]);
    };

    return (
        <div className={styles.container}>
            <div className={styles.messageList}>
                {messages.map((msg, index) => (
                    <Message key={index} message={msg.text} isUserMessage={msg.isUser} />
                ))}
            </div>
            <Input onSendMessage={handleSendMessage} />
        </div>
    );
};

export default Container;
