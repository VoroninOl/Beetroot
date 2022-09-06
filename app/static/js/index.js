

// Vue JS
const chat = new Vue({
    el: '#div-chat',
    delimiters: ['[[',']]'],
    data: {
        chatUsers: [],
        chatMessages: [],
        userChats: [],
        chatInput: '',
        chosenChat: 'General chat',
    },
    updated: setNamesListener,
    methods: {
        updateMessages: (data) => {
            chat.chatMessages = data
        },
        updateUsers: (data) => {
            chat.chatUsers = data
        },
        changeUserChat: (data) => {
            chat.chosenChat = data
        },
        updateUserChats: (data) => {
            
        },
        sendMessage: () => {
            if (chat.chatInput.length > 0){
                socket.send({'event': 'generalMessage', 'username': username, 'msg': chat.chatInput})
                chat.chatInput = ''
            }
        }
    }
})


// Sockets

const socket = io.connect('http://127.0.0.1:5000')
const username = $('#username').text()

socket.on('connect', () => {
    socket.send({'event': 'logged'})
})

socket.on('message', data => {
    console.log(data)
    chat.updateUsers(data.chatUsers)
    chat.updateMessages(data.chatHistory)
    // setNamesListener()
})





