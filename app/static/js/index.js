

// Vue JS
const chat = new Vue({
    el: '#div-chat',
    delimiters: ['[[',']]'],
    data: {
        chatUsers: [],
        chatMessages: [],
        mainChat: [],
        userChats: [],
        chatInput: '',
        choosenChat: 'General chat',
    },
    methods: {
        updateMessages: (mainChat, userChats) => {
            chat.mainChat = mainChat
            if (userChats){
                chat.userChats = userChats
            }
        },
        updateChatMessages: () => {
            if (chat.choosenChat === 'General chat'){
                chat.chatMessages = chat.mainChat
            }
            else {
                chat.chatMessages = chat.userChats[chat.choosenChat]
            }
        },
        updateUsers: (data) => {
            chat.chatUsers = data
        },
        changeUserChat: (data) => {
            chat.choosenChat = data
            chat.updateChatMessages()
        },
        updateUserChats: (data) => {
            
        },
        sendMessage: () => {
            if (chat.chatInput.length > 0){
                socket.send({'event': 'message', 'username': username, 'msg': chat.chatInput, 'receiver': chat.choosenChat})
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
    if (!data.privateMsgTo){
        chat.updateUsers(data.chatUsers)
        chat.updateMessages(data.chatHistory, data.userChats)
        chat.updateChatMessages()
    }
    else if (data.privateMsgTo === username || data.privateMsgFrom === username){
        socket.send({'event': 'updateUserChat'})
    }
    
})





