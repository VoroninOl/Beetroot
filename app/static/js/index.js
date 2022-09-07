

// Vue JS
const chat = new Vue({
    el: '#div-chat',
    delimiters: ['[[',']]'],
    data: {
        chatUsers: [],
        chatMessages: [],
        mainChat: [],
        userChats: [],
        newMessages: [],
        chatInput: '',
        choosenChat: 'General chat',
    },
    watch: {
        chatUsers: updateUsersInGraph
    },
    methods: {
        // Updating info in chats
        updateMessages: (data) => {
            chat.chatUsers = data.chatUsers
            chat.mainChat = data.chatHistory
            if (data.userChats){
                chat.userChats = data.userChats
            }
            chat.updateChatMessages()
        },
        // Shows messages of choosen chat
        updateChatMessages: () => {
            if (chat.choosenChat === 'General chat'){
                chat.chatMessages = chat.mainChat
            }
            else {
                chat.chatMessages = chat.userChats[chat.choosenChat]
            }
        },
        // Changing class to mark new messages
        markNewMessage: (user) => {
            if (chat.choosenChat !== user){
                chat.newMessages.push(user)
            }
        },
        // Changing opened chat
        changeUserChat: (user) => {
            chat.choosenChat = user
            chat.updateChatMessages()
            const userIndex = chat.newMessages.indexOf(user)
            if (userIndex !== -1) {
                chat.newMessages.splice(userIndex, 1)
            }
        },
        // Sending message to server
        sendMessage: () => {
            if (chat.chatInput.length > 0){
                socket.send({'event': 'message', 'username': username, 'msg': chat.chatInput, 'receiver': chat.choosenChat})
                chat.chatInput = ''
            }
        }
    }
})


// Cytoscape

const cy = cytoscape({
    container: $('#div-graph'),
    elements: {
        nodes: [],
        edges: [],
    },
    style: [ // the stylesheet for the graph
        {
            selector: 'node',
            style: {
                'background-color': '#666',
                'label': 'data(id)'
            }
        },

        {
            selector: '[name = "msg"]',
            style: {
                'height': '20px',
                'width': '35px',
                'background-color': '#666',
                'label': 'data(name)',
                'shape': 'rectangle'
            }
        },

        {
            selector: 'edge',
            style: {
                'width': 3,
                'line-color': '#ccc',
                'target-arrow-color': '#ccc',
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier'
            }
        }
    ],

    layout: {
        name: 'circle',
        fit: true,
        animate: true,
    }
})

// Sockets

const socket = io.connect(`http://${window.location.hostname}`)
const username = $('#username').text()

// Message on connection
socket.on('connect', () => {
    socket.send({'event': 'logged'})
})

// Handler of message receiving 
socket.on('message', data => {
    // Checks it is message to general chat
    if (!data.privateMsgTo){
        chat.updateMessages(data)
    }
    // Checks if user is sender of receiver of message
    else if (data.privateMsgTo === username || data.privateMsgFrom === username){
        socket.send({'event': 'updateUserChat'})
        updateChatsInGraph(data.privateMsgFrom, data.privateMsgTo)
        // Marking new message in chat if user is reveiver
        if (username === data.privateMsgTo){
            chat.markNewMessage(data.privateMsgFrom)
        }
    }
    else{
        // Updates edges in graph and plays animation of message
        updateChatsInGraph(data.privateMsgFrom, data.privateMsgTo)
    }
})

