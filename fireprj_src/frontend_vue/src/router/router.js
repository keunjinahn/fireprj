import Vue from 'vue'
import VueRouter from 'vue-router'
import * as View from '@/views'
import session from '@/plugins/session'
import { Typhoon_Manage } from "../views";

async function rootAccess(to, from, next) {
  if (!session.authentication && to.query.uid) {
    try {
      await session.loginFromProp(to.query.uid)
      next({ name: 'sensor_manage' })
    }
    catch (e) {
      next({ name: 'sensor_manage' })
    }
  }
  else next({ name: 'sensor_manage' })
}

const beforeEnter = (to, from, next) => {
  if (session.authentication) next()
  else next({ name: 'login' })
}

Vue.use(VueRouter)

const routes = [{
  path: '/',
  name: 'home',
  template: '<router-view />',
  beforeEnter: rootAccess
},
{
  path: '/login',
  component: View.Login,
  children: [
    {
      path: '',
      name: 'login',
      component: View.Login_SignIn
    },
    {
      path: 'signup',
      name: 'signup',
      component: View.Login_SignUp
    },
    {
      path: 'find-password',
      name: 'find-password',
      component: View.Login_FindPassword
    }
  ]
},
{
  path: '/manage',
  name: 'manage',
  component: View.SubView,
  redirect: { name: 'sensor_manage' },
  beforeEnter,
  children: [
    {
      path: 'sensor_manage',
      name: 'sensor_manage',
      component: View.SensorManage,
      meta: { breadcrumb: [{ text: '관리', disabled: true }, { text: '감지기 관리', disabled: true }] },
      props: true,
      beforeEnter
    },
    {
      path: 'repeater_manage',
      name: 'repeater_manage',
      component: View.RepeaterManage,
      meta: { breadcrumb: [{ text: '관리', disabled: true }, { text: '중계기 관리', disabled: true }] },
      props: true,
      beforeEnter
    },
    {
      path: 'receiver_manage',
      name: 'receiver_manage',
      component: View.ReceiverManage,
      meta: { breadcrumb: [{ text: '관리', disabled: true }, { text: '수신기 관리', disabled: true }] },
      props: true,
      beforeEnter
    },
  ]
},
{
  path: '/monitor',
  name: 'monitor',
  component: View.SubView,
  redirect: { name: 'sensor_event' },
  beforeEnter,
  children: [
    {
      path: 'sensor_event',
      name: 'sensor_event',
      component: View.SensorEvent,
      meta: { breadcrumb: [{ text: '모니터링', disabled: true }, { text: '실시간 이벤트', disabled: true }] },
      props: true,
      beforeEnter
    },
    {
      path: 'event_list',
      name: 'event_list',
      component: View.EventList,
      meta: { breadcrumb: [{ text: '모니터링', disabled: true }, { text: '이벤트 리스트', disabled: true }] },
      props: true,
      beforeEnter
    },
  ]
},
{
  path: '/sensor_analysis',
  name: 'sensor_analysis',
  component: View.SensorAnalysis,
  meta: { breadcrumb: [{ text: '데이터 분석', disabled: true }, { text: '이벤트 분석', disabled: true }] },
  props: true,
  beforeEnter
},
{
  path: '/user_manage',
  name: 'user_manage',
  component: View.UserManage,
  meta: { breadcrumb: [{ text: 'CRM', disabled: true }, { text: '사용자 관리', disabled: true }] },
  props: true,
  beforeEnter
},
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
