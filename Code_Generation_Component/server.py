from flask import Flask, render_template
app = Flask(__name__, static_folder='static',
            template_folder='templates')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/my-link/')
def my_link():
    from os import listdir
    from numpy import array
    from keras.preprocessing.text import Tokenizer, one_hot
    from keras_preprocessing.sequence import pad_sequences
    from keras.models import Model
    from keras.utils import to_categorical
    from keras.layers import Embedding, TimeDistributed, RepeatVector, LSTM, concatenate , Input, Reshape, Dense, Flatten
    from keras.utils import array_to_img, img_to_array, load_img
    from keras.applications.inception_resnet_v2 import InceptionResNetV2, preprocess_input
    import numpy as np
    import tensorflow as tf

    model = tf.keras.models.load_model('saved_model')

    # Load the images and preprocess them for inception-resnet
    images = []
    all_filenames = listdir('images-new-3/')
    all_filenames.sort()
    for filename in all_filenames:
        images.append(img_to_array(load_img('images-new-3/'+filename, target_size=(299, 299))))
    images = np.array(images, dtype=float)
    images = preprocess_input(images)

    # Run the images through inception-resnet and extract the features without the classification layer
    IR2 = InceptionResNetV2(weights='imagenet', include_top=False)

    features = IR2.predict(images)

    # We will cap each input sequence to 100 tokens
    #max_caption_len = 100
    max_caption_len = 100
    # Initialize the function that will create our vocabulary 
    tokenizer = Tokenizer(filters='', split=" ", lower=False)

    # Read a document and return a string
    def load_doc(filename):
        file = open(filename, 'r')
        text = file.read()
        file.close()
        return text

    # Load all the HTML files
    X = []
    all_filenames = listdir('html-new-3/')
    all_filenames.sort()
    for filename in all_filenames:
        X.append(load_doc('html-new-3/'+filename))

    # Create the vocabulary from the html files
    tokenizer.fit_on_texts(X)

    # Add +1 to leave space for empty words
    vocab_size = len(tokenizer.word_index) + 1
    # Translate each word in text file to the matching vocabulary index
    sequences = tokenizer.texts_to_sequences(X)
    # The longest HTML file
    max_length = max(len(s) for s in sequences)

    # Intialize our final input to the model
    X, y, image_data = list(), list(), list()
    for img_no, seq in enumerate(sequences):
        for i in range(1, len(seq)):
            # Add the entire sequence to the input and only keep the next word for the output
            in_seq, out_seq = seq[:i], seq[i]
            # If the sentence is shorter than max_length, fill it up with empty words
            in_seq = pad_sequences([in_seq], maxlen=max_length)[0]
            # Map the output to one-hot encoding
            out_seq = to_categorical([out_seq], num_classes=vocab_size)[0]
            # Add and image corresponding to the HTML file
            image_data.append(features[img_no])
            # Cut the input sentence to 100 tokens, and add it to the input data
            X.append(in_seq[-100:])
            y.append(out_seq)

    X, y, image_data = np.array(X), np.array(y), np.array(image_data)

    def word_for_id(integer, tokenizer):
        for word, index in tokenizer.word_index.items():
            if index == integer:
                return word
        return None

    # generate a description for an image
    def generate_desc(model, tokenizer, photo, max_length):
        toprint = ""
        # seed the generation process
        in_text = 'START'
        # iterate over the whole length of the sequence
        for i in range(max_length):
            # integer encode input sequence
            sequence = tokenizer.texts_to_sequences([in_text])[0][-100:]
            # pad input
            sequence = pad_sequences([sequence], maxlen=max_length)
            # predict next word
            yhat = model.predict([photo,sequence], verbose=0)
            # convert probability to integer
            yhat = np.argmax(yhat)
            # map integer to word
            word = word_for_id(yhat, tokenizer)
            # stop if we cannot map the word
            if word is None:
                break
            # append as input for generating the next word
            in_text += ' ' + word
            # Print the prediction
            print(' ' + word, end='')
            toprint += word
            toprint += ' '
            # stop if we predict the end of the sequence
            if word == 'END':
                break
        return toprint

    def makeFile (a):
        import os.path

        with open(os.path.dirname(__file__) + "\..\client\src\TextEditor.js") as f:
            lines = f.readlines();
            
        with open(os.path.dirname(__file__) +  "\..\client\src\TextEditor.js", "w") as f:
            lines.insert(0, 
            """
        import {useCallback, useEffect, useState} from 'react'
        import Quill from 'quill'
        import "quill/dist/quill.snow.css"
        import {io} from 'socket.io-client'

        const TOOLBAR_OPTIONS = [
            [{ header: [1, 2, 3, 4, 5, 6, false] }],
            [{ font: [] }],
            [{ list: "ordered" }, { list: "bullet" }],
            ["bold", "italic", "underline"],
            [{ color: [] }, { background: [] }],
            [{ script: "sub" }, { script: "super" }],
            [{ align: [] }],
            ["image", "blockquote", "code-block"],
            ["clean"],
        ]

        export default function TextEditor() {
            const [socket, setSocket] = useState()
            const [quill, setQuill] = useState()

            useEffect(() => {
                const s = io("http://localhost:3001")
                setSocket(s)

                return() => {
                    s.disconnect()
                }
            }, [])



            useEffect (() => {

                if (socket == null || quill == null) return

                const handler = (delta) => {
                    quill.updateContents (delta)
                }

                socket.on ('receive-changes',handler)

                return() => {
                socket.off ('receive-changes', handler)
                }
            }, [socket, quill])



            useEffect (() => {

                if (socket == null || quill == null) return

                const handler = (delta, oldDelta, source) => {
                    if (source !== 'user') return

                    if (delta.ops[1].insert === 'x') {
                        delta.ops[1].insert = ' """ + a + """ '
                    }
                    console.log (delta.ops[1].insert);
                    socket.emit("send-changes", delta)

                }
                quill.on ('text-change',handler)

                return() => {
                    quill.off ('text-change', handler)
                }
            }, [socket, quill])

            const wrapperRef = useCallback ((wrapper) => {
                if (wrapper == null) return

                wrapper.innerHTML = ""
                const editor = document.createElement("div")
                wrapper.append (editor)
                const q = new Quill(editor, {theme: 'snow', modules: {toolbar: TOOLBAR_OPTIONS}})
                setQuill(q)

            }, [])

        return (
            <div className = "container" ref={wrapperRef}></div>
        )
        }
        """)
            f.write("\n".join(lines))

            
        

    test_image = img_to_array(load_img('images-test/test.jpg', target_size=(299, 299)))
    test_image = np.array(test_image, dtype=float)
    test_image = preprocess_input(test_image)
    test_features = IR2.predict(np.array([test_image]))
    #generate_desc(model, tokenizer, np.array(test_features), 100)
    a = generate_desc(model, tokenizer, np.array(test_features), 100)

    makeFile (a)

    a+= "<br> <center> <a href = 'http://localhost:5000'>Back</a> </center>"
    a+= "<br> <center> <a href = 'http://localhost:3000'>Open code in code editor</a> </center>"
    #a+= "<br> <center> <a href = 'http://localhost:3000'>Open in code editor</a> </center>"
    return a



if __name__ == '__main__':
  app.run(debug=True)