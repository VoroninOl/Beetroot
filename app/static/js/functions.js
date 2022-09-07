

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