from flask import Flask, render_template, request, jsonify
import spacy

# 加载 spaCy 的英语模型
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

def annotate_sentence(sentence):
    doc = nlp(sentence)
    annotated_sentence = []
    noun_chunks_spans = {chunk.start: chunk.end for chunk in doc.noun_chunks}  # 记录名词短语的起始和结束索引

    i = 0
    while i < len(doc):
        token = doc[i]

        # 如果是介词，并且后面跟着一个名词短语
        if token.pos_ == "ADP" and token.dep_ == "prep":
            # 将括号用 <strong> 包裹，但介词保持红色且不加粗
            annotated_sentence.append(f"<strong>(</strong><span style='color: red;'>{token.text}</span>")
            
            # 查找介词后的名词短语
            if i + 1 in noun_chunks_spans:
                chunk_end = noun_chunks_spans[i + 1]
                noun_chunk_text = ' '.join([doc[j].text for j in range(i + 1, chunk_end)])
                annotated_sentence.append(f"<strong style='color: black;'>{noun_chunk_text}</strong>")
                annotated_sentence.append("<strong>)</strong>")
                i = chunk_end  # 跳过整个名词短语的词
                continue
            else:
                annotated_sentence.append("<strong>)</strong>")  # 如果没有找到名词短语，直接闭合括号

        # 检查是否属于名词短语
        elif i in noun_chunks_spans:
            chunk_end = noun_chunks_spans[i]
            noun_chunk_text = ' '.join([doc[j].text for j in range(i, chunk_end)])
            annotated_sentence.append(f"<strong style='color: black;'>{noun_chunk_text}</strong>")
            i = chunk_end  # 跳过整个名词短语的词
            continue

        # 标记谓语动词
        elif token.dep_ in ("ROOT", "aux", "auxpass", "advcl"):
            annotated_sentence.append(f"<strong style='color: darkred;'>{token.text}</strong>")

        else:
            # 其他部分保持原样
            annotated_sentence.append(token.text)

        i += 1

    # 使用空格将标注后的 token 重新连接成句子
    return ' '.join(annotated_sentence)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/annotate', methods=['POST'])
def annotate():
    data = request.get_json()
    sentence = data['sentence']
    
    # 标注句子
    annotated = annotate_sentence(sentence)
    
    # 返回JSON格式的标注结果
    return jsonify({'annotated_sentence': annotated})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7089, debug=True)
