<template>
    <div class="status-chip-container">
        <v-chip v-for="(s, i) in status" :key="i" :color="s.color" label small dark style="width: 100%" class="status-chip">
            <v-icon left small v-text="s.icon"></v-icon>
            {{s.text}}
        </v-chip>
    </div>
</template>

<script>
import _ from 'lodash'
export default {
    props: {
        collector: {
            type: Object,
            required: true
        }
    },
    methods: {
        calculate () {
            let {device, _tra} = this.collector
            let tra_conn = (_tra.conn & 1) ? '.' : ''
            let code = this.$session.parseStatusCode(device.COLCTTRMNL_STATUS)
            if (!code.length) {
                this.status = [{
                    color: 'green',
                    icon: 'mdi-play-circle-outline',
                    text: '정상' + tra_conn
                }]
                return;
            }

            if (_.includes(code, '317')) {
                this.status = [{
                    color: 'grey',
                    icon: 'mdi-stop-circle-outline',
                    text: '끊어짐' + tra_conn
                }]
                return;
            }

            for (let c of code) {
                let pb = _.find(this.$session.pb, {code: c})
                this.status.push({
                    color: 'orange',
                    icon: 'mdi-alert',
                    text: pb.short
                })
            }
        }
    },
    mounted () {
        this.calculate()
    },
    data () {
        return {
            status: []
        }
    }
}
</script>

<style lang="scss" scoped>
    .status-chip-container{
        padding: 2px 0}
    .status-chip{
        margin: 2px 0}
</style>