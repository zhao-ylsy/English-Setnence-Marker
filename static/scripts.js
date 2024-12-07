document.addEventListener('DOMContentLoaded', function() {
    const annotateButton = document.getElementById('annotateButton');
    const clearButton = document.getElementById('clearButton');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const output = document.getElementById('annotatedOutput');
    const inputText = document.getElementById('inputText');

    // 按钮点击事件
    annotateButton.addEventListener('click', annotateSentence);
    clearButton.addEventListener('click', clearFields);

    function clearFields() {
        inputText.value = '';
        output.innerHTML = '';
        inputText.style.borderColor = '#e0e6ed';
        inputText.focus();
    }

    function annotateSentence() {
        const sentence = inputText.value;

        // 输入为空时的处理
        if (!sentence.trim()) {
            output.innerHTML = 'Please enter a sentence.';
            inputText.focus();
            inputText.style.borderColor = '#e74c3c';
            return;
        }

        // 显示加载动画
        loadingSpinner.style.display = 'block';
        annotateButton.disabled = true;
        clearButton.disabled = true;
        output.innerHTML = '';

        // 发送请求到后端
        fetch('/annotate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ sentence: sentence })
        })
        .then(response => response.json())
        .then(data => {
            output.innerHTML = data.annotated_sentence;
        })
        .catch(error => {
            output.innerHTML = 'An error occurred. Please try again.';
            console.error('Error:', error);
        })
        .finally(() => {
            loadingSpinner.style.display = 'none';
            annotateButton.disabled = false;
            clearButton.disabled = false;
            inputText.style.borderColor = '#e0e6ed';
        });
    }
});
