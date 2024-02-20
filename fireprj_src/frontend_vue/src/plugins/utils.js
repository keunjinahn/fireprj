import _ from 'lodash'
import numeral from 'numeral'

const regx_end_session = /^Ended\sdesktop\ssession\s"(.*)"\sfrom\s(.*)\sto\s(.*),\s(\d+)\s(.*)$/
const regx_start_remote = /^Started\sremote\sdesktop\swithout\snotification\s\((.*)\)$/
const regx_start_session = /^Started\sdesktop\ssession\s"(.*)"\sfrom\s(.*)\sto\s(.*)$/

export default {
  install(Vue) {
    Vue.filter('format', (value, option) => {
      if (!option) option = '0,0'
      return numeral(value).format(option)
    })
    Vue.prototype.$numeral = numeral

    Vue.prototype.$getColor = (cost) => {
      var cost_array = [10000000, 20000000, 50000000, 100000000]
      if (cost < cost_array[0])
        return 'cost_color_1'
      else if (cost >= cost_array[0] && cost <= cost_array[1])
        return 'cost_color_2'
      else if (cost >= cost_array[1] && cost <= cost_array[2])
        return 'cost_color_3'
      else if (cost >= cost_array[2] && cost < cost_array[3])
        return 'cost_color_4'
      else
        return 'cost_color_5'
    }
    Vue.prototype.$getLevel = (cost) => {
      var cost_array = [10000000, 20000000, 50000000, 100000000]
      if (cost < cost_array[0])
        return 1
      else if (cost >= cost_array[0] && cost <= cost_array[1])
        return 2
      else if (cost >= cost_array[1] && cost <= cost_array[2])
        return 3
      else if (cost >= cost_array[2] && cost < cost_array[3])
        return 4
      else
        return 5
    }
    Vue.prototype.$getCostColor = (cost) => {
      var cost_array = [10000000, 20000000, 50000000, 100000000]
      if (cost < cost_array[0])
        return 'cost_color_1'
      else if (cost >= cost_array[0] && cost <= cost_array[1])
        return 'cost_color_2'
      else if (cost >= cost_array[1] && cost <= cost_array[2])
        return 'cost_color_3'
      else if (cost >= cost_array[2] && cost < cost_array[3])
        return 'cost_color_4'
      else
        return 'cost_color_5'
    }

    Vue.prototype.$getCostRange = (cost) => {
      var cost_array = [10000000, 20000000, 50000000, 100000000]
      if (cost < cost_array[0])
        return '규모 1(관심)'
      else if (cost >= cost_array[0] && cost <= cost_array[1])
        return '규모 2(주의)'
      else if (cost >= cost_array[1] && cost <= cost_array[2])
        return '규모 3(경계)'
      else if (cost >= cost_array[2] && cost < cost_array[3])
        return '규모 4(위험)'
      else
        return '규모 5(심각)'
    }


    Vue.prototype.$getTextColor = (cost) => {
      var cost_array = [10000000, 20000000, 50000000, 100000000]
      if (cost < cost_array[0])
        return 'blue--text'
      else if (cost >= cost_array[0] && cost <= cost_array[1])
        return 'amber--text'
      else if (cost >= cost_array[1] && cost <= cost_array[2])
        return 'yellow--text'
      else if (cost >= cost_array[2] && cost < cost_array[3])
        return 'deep-orange--text'
      else
        return 'red--text'
    }
    Vue.prototype.$decodeHTMLEntities = (str) => {
      if (str !== undefined && str !== null && str !== '') {
        str = String(str);

        str = str.replace(/<script[^>]*>([\S\s]*?)<\/script>/gmi, '');
        str = str.replace(/<\/?\w(?:[^"'>]|"[^"]*"|'[^']*')*>/gmi, '');
        var element = document.createElement('div');
        element.innerHTML = str;
        str = element.textContent;
        element.textContent = '';
      }

      return str;
    }

    Vue.filter('transit', (value) => {
      let matched = regx_end_session.exec(value)
      if (matched) {
        let unit = ''
        if (_.startsWith(matched[5], 'sec')) unit = '초'
        else if (_.startsWith(matched[5], 'min')) unit = '분'
        else if (_.startsWith(matched[5], 'hour')) unit = '시간'
        return `"${matched[1]}" 세션이 종료되었습니다(${matched[2]} > ${matched[3]}, ${matched[4]} ${unit})`
      }

      matched = regx_start_remote.exec(value)
      if (matched) {
        return `원격제어를 시작합니다(${matched[1]})`
      }

      matched = regx_start_session.exec(value)
      if (matched) {
        return `원격 세션이 연결되었습니다(${matched[1]} > ${matched[2]})`
      }

      return value
    })
  }
}
