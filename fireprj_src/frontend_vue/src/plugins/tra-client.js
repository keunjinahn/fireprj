import Vue from 'vue'
export default new Vue({

    methods: {
        onOpen() {
            console.log('[ON OPEN]');
            this.$emit('open')
            this.state = 2
            this.pingTimer = setInterval(() => {
                this.pingCount += 1
                this.ws.send(JSON.stringify({
                    action: 'ping'
                }))
            }, 30 * 1000);

            this.send({
                action: 'authcookie'
            })

            this.send({
                action: 'logincookie'
            })
        },
        async onMessage(ev) {
            try {
                let data = JSON.parse(typeof ev.data === 'string' ? ev.data : await ev.data.text())
                if (data.action === 'pong') return;
                if (data.action === 'authcookie') return (this.authcookie = data.cookie)
                if (data.action === 'logincookie') return (this.logincookie = data.cookie)
                console.log(`[ON MESSAGE ${data.action}]`)
                if (data.action) {
                    if (data.action === 'nodes') {
                        let sum = []
                        for (let key in data.nodes) {
                            sum = sum.concat(data.nodes[key])
                        }
                        this.nodes = sum
                    }
                    this.$emit(data.action, data)
                } else console.log(data)
            } catch (e) {
                console.error(e)
            }
        },
        onError() {
            console.log('[ON ERROR]')
        },
        onClose() {
            clearInterval(this.pingTimer)
            console.log('[ON CLOSE]')
            this.ws = null
            this.state = 1
        },
        send(command) {
            try {
                this.ws.send(JSON.stringify(command))
            } catch (ex) {
                throw ex
            }
        },
        connect() {
            if (this.state === 2) return;
            let domain = process.env.VUE_APP_WS_DOMAIN ? '/' + process.env.VUE_APP_WS_DOMAIN : ''
            const host = `${process.env.VUE_APP_WS_ADDR}${domain}${process.env.VUE_APP_WS_CONTROL}`
            this.ws = new WebSocket(`${host}?user=${process.env.VUE_APP_WS_USERID}&pass=${process.env.VUE_APP_WS_USERPW}`)
            this.ws.onopen = this.onOpen
            this.ws.onmessage = this.onMessage
            this.ws.onerror = this.onError
            this.ws.onclose = this.onClose
        },
        getNode(nodeid) {
            if (!this.nodes) return null
            let node = this.nodes.filter(v => v._id === nodeid)
            if (node.length) return node[0]
            else return null
        },
        nodeKeyToId(nodeKey) {
            return `node/${process.env.VUE_APP_WS_DOMAIN}/${nodeKey}`
        }
    },
    data() {
        return {
            ws: null,
            state: 0,
            pingTimer: null,
            pingCount: 0,
            nodes: null,
            authcookie: null,
            logincookie: null
        }
    }
})