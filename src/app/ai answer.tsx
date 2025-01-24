const handleSendMessage = async (message: string) => {
    if (!message || isLoading) return;
  
    setIsLoading(true);
  
    // 사용자 메시지 추가
    const tempUserMessage = {
      messageId: `user-${Date.now()}`,
      userMessage: message,
      aiMessage: null,
    };
    addMessage(tempUserMessage);
  
    // API 요청 데이터 구성
    const payload = {
      question: message,
      brand: selectedBrand || null,
      model: selectedModel || null,
      userId: 1234, // 필요 시 사용자 ID 설정
      sessionId: currentSession?.sessionId || null,
    };
  
    console.log('Sending API Request with Payload:', payload);
  
    try {
      // API 호출
      const response = await fetch('http://localhost:8000/api/chat/answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
  
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Failed to fetch AI response:', response.statusText, errorText);
        return;
      }
  
      const result = await response.json();
      console.log('API Response:', result);
  
      // AI 응답 메시지 추가
      if (result?.answer) {
        const aiMessage = {
          messageId: `ai-${result.messageId}`, // API에서 반환한 messageId 사용
          userMessage: message, // 사용자가 보낸 메시지
          aiMessage: result.answer, // AI 응답 메시지
          keywords: result.keywords || [], // 키워드 리스트
          suggestedQuestions: result.suggestQuestions || [], // 추천 질문 리스트
        };
        addMessage(aiMessage);
      } else {
        console.error('API Response missing "answer" field', result);
      }
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };
  