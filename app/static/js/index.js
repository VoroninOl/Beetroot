
// Functions

function updateUsersInGraph(){
    let nodes = []
    for (const user of chat.chatUsers){
        nodes.push({data: {id: user, name: 'user'}})
    }
    cy.add(nodes)
    for (const node of cy.nodes()){
        if (!chat.chatUsers.includes(node.id()) && node.data().name!='msg'){
            cy.remove(node)
        }
    }
    cy.nodes('[name = "user"]').layout({
        name: 'circle',
        fit: true,
        animate: true,
    }).run()
}


function updateChatsInGraph(sender, receiver){
    if (cy.edges('#' + sender + receiver).length === 0){
        const edge = {data: {id: sender + receiver, source: sender, target: receiver}}
        cy.add(edge)
    }
    let x = cy.nodes('#' + sender).position().x
    let y = cy.nodes('#' + sender).position().y
    const msg = cy.add({data: { name: 'msg' }, position: {
        x: x,
        y: y
    }})
    msg.animate({
        position: cy.nodes('#' + receiver).position()
    },
    {
        duration: 900
    })
    setTimeout(() => {
        cy.remove(msg)
      }, 900)
}


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
        updateMessages: (data) => {
            chat.chatUsers = data.chatUsers
            chat.mainChat = data.chatHistory
            if (data.userChats){
                chat.userChats = data.userChats
            }
            chat.updateChatMessages()
        },
        updateChatMessages: () => {
            if (chat.choosenChat === 'General chat'){
                chat.chatMessages = chat.mainChat
            }
            else {
                chat.chatMessages = chat.userChats[chat.choosenChat]
            }
        },
        markNewMessage: (user) => {
            if (chat.choosenChat !== user){
                chat.newMessages.push(user)
            }
        },
        changeUserChat: (user) => {
            chat.choosenChat = user
            chat.updateChatMessages()
            const userIndex = chat.newMessages.indexOf(user)
            if (userIndex !== -1) {
                chat.newMessages.splice(userIndex, 1)
            }
        },
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

const socket = io.connect('http://127.0.0.1:5000')
const username = $('#username').text()

socket.on('connect', () => {
    socket.send({'event': 'logged'})
})

socket.on('message', data => {
    console.log(data)
    if (!data.privateMsgTo){
        chat.updateMessages(data)
    }
    else if (data.privateMsgTo === username || data.privateMsgFrom === username){
        socket.send({'event': 'updateUserChat'})
        updateChatsInGraph(data.privateMsgFrom, data.privateMsgTo)
        if (username === data.privateMsgTo){
            chat.markNewMessage(data.privateMsgFrom)
        }
    }
    else{
        updateChatsInGraph(data.privateMsgFrom, data.privateMsgTo)
    }
})

