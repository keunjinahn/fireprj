<template>
    <div>
    </div>
</template>

<script>
export default {
    components: {},
    methods: {
        async getData () {
            let {data} = await this.$http.get('dashboard/error_summary')
            this.cnt.dev_err = data.dev_err
            this.cnt.disconnected_err = data.disconnected_err
            this.cnt.disk_err = data.disk_err
            this.cnt.measure_data_err = data.measure_data_err
            this.cnt.measure_na_err = data.measure_na_err
            this.cnt.all_cnt = data.all_cnt
            this.updatedAt = Date.now()
            console.log(`[SUMMARY REFRESH @${this.updatedAt}]`)

            if (!this.firstLoad && this.$session.settings.dashboard.enable_alarm_popup) {
                this.ReportPopupOpen = true
                this.firstLoad = true
                sessionStorage.setItem('alerm', 1)
            }
        },
        async getE1Data () {
            let params = {type: 'dev_err'}
            let {data} = await this.$http.get('dashboard/error_detail', {params})
            this.e1.data = data
            this.e1.loading = false
        },
        async getE2Data () {
            let params = {type: 'measure_na_err'}
            let {data} = await this.$http.get('dashboard/error_detail', {params})
            this.e2.data = data
            this.e2.loading = false
        },
        async getE3Data () {
            let params = {type: 'measure_data_err'}
            let {data} = await this.$http.get('dashboard/error_detail', {params})
            this.e3.data = data
            this.e3.loading = false
        },
        async getE4Data () {
            let params = {type: 'disk_err'}
            let {data} = await this.$http.get('dashboard/error_detail', {params})
            this.e4.data = data
            this.e4.loading = false
        },
        async getE5Data () {
            let params = {type: 'disconnected_err'}
            let {data} = await this.$http.get('dashboard/error_detail', {params})
            this.e5.data = data
            this.e5.loading = false
        },
        async getStatusSummary () {
            let {data} = await this.$http.get('dashboard/status_summary')
            this.cnt.ABNORMAL_CNT = data.ABNORMAL_CNT
            this.cnt.DATA_TOTAL = data.DATA_TOTAL
            this.cnt.NORMAL_CNT = data.NORMAL_CNT
            this.cnt.SUBSTI_CNT = data.SUBSTI_CNT

            this.cnt.OPERATION_RATE = data.OPERATION_RATE
            this.cnt.TROUBLE_RATE = data.TROUBLE_RATE
            this.cnt.OPERATION_MONTH_RATE = data.OPERATION_MONTH_RATE
            this.cnt.TROUBLE_MONTH_RATE = data.TROUBLE_MONTH_RATE
        },
        clickHandler (values) {
            if (this.$route.name === 'device') {
                this.$session.$emit('device-tab-reset')
            }
            if (!values) this.$router.push({name: 'device', query: {}})
            if (this.$route.query.fstatus && this.$route.query.fstatus === values) return;
            this.$router.push({name: 'device', query: {fstatus: values}})
        }
    },
    watch: {
        'e1.show': {
            handler () {
                if (this.e1.show && !this.e1.loading) {
                    this.e1.loading = true
                    this.getE1Data()
                }
            }
        },
        'e2.show': {
            handler () {
                if (this.e2.show && !this.e2.loading) {
                    this.e2.loading = true
                    this.getE2Data()
                }
            }
        },
        'e3.show': {
            handler () {
                if (this.e3.show && !this.e3.loading) {
                    this.e3.loading = true
                    this.getE3Data()
                }
            }
        },
        'e4.show': {
            handler () {
                if (this.e4.show && !this.e4.loading) {
                    this.e4.loading = true
                    this.getE4Data()
                }
            }
        },
        'e5.show': {
            handler () {
                if (this.e5.show && !this.e5.loading) {
                    this.e5.loading = true
                    this.getE5Data()
                }
            }
        }
    },
    mounted () {
        /*
        if (this.timer) {
            clearInterval(this.timer)
            this.timer = null
        }
        this.timer = setInterval(() => {
            this.getData()
            this.getStatusSummary()
        }, 300 * 1000)
        this.getData()
        this.getStatusSummary()
        */
    },
    data () {
        return {
            firstLoad: sessionStorage.getItem('alerm') ? true : false,
            ReportPopupOpen: false,
            timer: null,
            cnt: {
                // error summary
                dev_err: 0,
                disconnected_err: 0,
                disk_err: 0,
                measure_data_err: 0,
                measure_na_err: 0,
                all_cnt: 0,

                // status summary
                ABNORMAL_CNT: 0,
                DATA_TOTAL: 0,
                NORMAL_CNT: 0,
                SUBSTI_CNT: 0,

                // 가동률, 장애율
                OPERATION_RATE: 0,
                TROUBLE_RATE: 0,
                OPERATION_MONTH_RATE: 0,
                TROUBLE_MONTH_RATE: 0
            },
            updatedAt: Date.now(),
            e1: {
                show: false,
                loading: false,
                data: []
            },
            e2: {
                show: false,
                loading: false,
                data: []
            },
            e3: {
                show: false,
                loading: false,
                data: []
            },
            e4: {
                show: false,
                loading: false,
                data: []
            },
            e5: {
                show: false,
                loading: false,
                data: []
            },
            e6: {
                show: false,
                loading: false,
                data: []
            }
        }
    }
}
</script>

<style lang="scss" scoped>
    .status-summary {
        display: inline-block;
        background-color: white;
        border-radius: 20px;
        color: black;
        font-size: 12px;
        padding: 0 20px;
    }
    
</style>