<template>
  <div ref="desktop" class="desktop" :class="{fullscreen: onControl}">
    <div class="desktop-wrap">
      <div class="desktop-on-control">
        <v-btn icon dark @click="releaseFullscreen">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </div>
      <div class="desktop-state">
        <v-btn
          color="grey lighten-2"
          outlined
          tile
          v-if="state.value < 3"
          :loading="state.value !== 0"
          @click="start"
        >{{state.text}}</v-btn>
        <div v-else class="viewmode-control">
          <v-btn icon large color="white" @click="start">
            <v-icon large>mdi-close</v-icon>
          </v-btn>
          <v-btn fab small color="primary" @click="startControl">
            <v-icon>mdi-mouse</v-icon>
          </v-btn>
        </div>
      </div>
      <canvas
        ref="screen"
        class="desktop-screen"
        width="640"
        height="480"
        @contextmenu="() => false"
        @mousedown="mouseDownHandler"
        @mouseup="mouseUpHandler"
        @mousemove="mouseMoveHandler"
        @mousewheel="houseWheelHandler"
      />
    </div>
  </div>
</template>

<script>
// import CreateAmtRedirect from "@/plugins/amt-redir-ws";
// import CreateAmtRemoteDesktop from "@/plugins/amt-desktop";
import CreateAgentRedirect from "@/plugins/agent-redir-ws";
import CreateAgentRemoteDesktop from "@/plugins/agent-desktop";

let dblClickDetectArgs = {
  t: 0,
  x: 0,
  y: 0
};

export default {
  props: {
    node: {
      type: Object,
      required: true
    }
  },
  methods: {
    start() {
      if (this.desk) {
        this.desk.Stop();
        this.desk = null;
        return;
      }
      this.desk = CreateAgentRedirect(
        this.$control,
        CreateAgentRemoteDesktop(`kvmid_${this.shortid}`),
        `${process.env.VUE_APP_WS_HOST}:${process.env.VUE_APP_WS_PORT}`,
        this.$control.authcookie,
        `/${process.env.VUE_APP_WS_DOMAIN}`
      );
      this.desk.shortid = this.shortid;
      this.desk.attemptWebRTC = true; // attemptWebRTC  features & 128 ;
      this.desk.onStateChanged = this.onMultiDesktopStateChange.bind(this);
      this.desk.m.CompressionLevel = this.settings.quality;
      this.desk.m.ScalingLevel = this.settings.scaling;
      this.desk.m.FrameRateTimer = this.settings.framerate;
      // if (debugmode > 0) {
      //   desk.m.onScreenSizeChange = mdeskAdjust;
      // } // Multi-Desktop Adjust
      this.desk.Start(this.node._id);
      this.desk.contype = 1;
      // multiDesktop[nodeid] = desk;
    },
    startControl() {
      if (this.$refs.desktop.requestFullscreen)
        this.$refs.desktop.requestFullscreen();
      else if (this.$refs.desktop.mozRequestFullScreen)
        this.$refs.desktop.mozRequestFullScreen();
      else if (this.$refs.desktop.webkitRequestFullscreen)
        this.$refs.desktop.webkitRequestFullscreen();
      else if (this.$refs.desktop.msRequestFullscreen)
        this.$refs.desktop.msRequestFullscreen();
      else return console.error("cannot fullscreen");

      document.onkeypress = (evt) => { this.desk.m.handleKeyPress(evt) };
      document.onkeydown = (evt) => { this.desk.m.handleKeyDown(evt) };
      document.onkeyup = (evt) => { this.desk.m.handleKeyUp(evt) };

      this.$nextTick(() => {
        this.onControl = true;

        let {innerWidth, innerHeight} = window
        let {width, height} = this.$refs.screen

        if ((innerHeight / innerWidth) > (height / width)) {
            let hNew = ((height * innerWidth) / width) + 'px';
            this.$refs.screen.style.height = hNew;
            this.$refs.screen.style.width = '100%';
        }
        else {
            let wNew = ((width * innerHeight) / height) + 'px';
            this.$refs.screen.style.height = null;
            this.$refs.screen.style.width = wNew;
        }
      });
    },
    releaseFullscreen () {
      if (document.exitFullscreen) document.exitFullscreen();
      else if (document.mozCancelFullScreen) document.mozCancelFullScreen();
      else if (document.webkitExitFullscreen) document.webkitExitFullscreen();
      else if (document.msExitFullscreen) document.msExitFullscreen();
      else return console.error("cannot fullscreen");
    },
    fullscreenChangeHandler() {
      let is_fullscreen = !!document.fullscreenElement;
      if (!is_fullscreen) {
        this.onControl = false;
        this.$refs.screen.style.height = null;
        this.$refs.screen.style.width = null;

        document.onkeypress = null;
        document.onkeydown = null;
        document.onkeyup = null;
      }
    },
    onMultiDesktopStateChange(desk, state) {
      this.state.value = state;
      this.state.text = [
        "클릭하여 화면보기",
        "연결 중...",
        "설정 중...",
        false,
        false
      ][Math.min(state, 4)];
    },
    eventModifier(evt) {
      evt.addx = 0;
      evt.addy = 0;
    },
    dblClickDetect(evt) {
      if (evt.buttons != 1) return;
      let t = Date.now();
      if (
        t - dblClickDetectArgs.t < 250 &&
        Math.abs(evt.clientX - dblClickDetectArgs.x) < 2 &&
        Math.abs(evt.clientY - dblClickDetectArgs.y) < 2
      ) {
        this.desk.m.mousedblclick(evt);
      }
      dblClickDetectArgs.t = t;
      dblClickDetectArgs.x = evt.clientX;
      dblClickDetectArgs.y = evt.clientY;
    },
    mouseDownHandler(evt) {
      if (this.state.value !== 3) return;
      this.eventModifier(evt);
      this.desk.m.mousedown(evt);
    },
    mouseUpHandler(evt) {
      if (this.state.value !== 3) return;
      this.eventModifier(evt);
      this.desk.m.mouseup(evt);
    },
    mouseMoveHandler(evt) {
      if (this.state.value !== 3) return;
      this.eventModifier(evt);
      this.desk.m.mousemove(evt);
    },
    houseWheelHandler(evt) {
      if (this.state.value !== 3) return;
      this.eventModifier(evt);
      this.desk.m.mousewheel(evt);
      if (evt.preventDefault) evt.preventDefault();
      if (evt.stopPropagation) evt.stopPropagation();
    }
  },
  mounted() {
    this.shortid = this.node._id.split("/")[2];
    this.$refs.screen.id = `kvmid_${this.shortid}`;
    document.onwebkitfullscreenchange = this.fullscreenChangeHandler.bind(this);
    document.onmozfullscreenchange = this.fullscreenChangeHandler.bind(this);
    document.onmsfullscreenchange = this.fullscreenChangeHandler.bind(this);
    document.onfullscreenchange = this.fullscreenChangeHandler.bind(this);
  },
  beforeDestroy() {
    if (this.desk) {
      this.desk.Stop();
      this.desk = null;
    }
    document.onwebkitfullscreenchange = null;
    document.onmozfullscreenchange = null;
    document.onmsfullscreenchange = null;
    document.onfullscreenchange = null;
  },
  data() {
    return {
      shortid: null,
      desk: null,
      settings: {
        encoding: "2",
        framerate: "50",
        quality: "50",
        scaling: "1024",
        showcad: true,
        showfocus: false,
        showmouse: true
      },
      state: {
        value: 0,
        text: "클릭하여 화면보기"
      },
      onControl: false
    };
  }
};
</script>

<style lang="scss" scoped>
  .desktop {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    background-color: black;
    margin-right: 15px;

    .desktop-wrap {
      position: relative;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    
    .desktop-on-control {
      display: none;
      position: absolute;
      top: 5px;
      right: 5px;
      border-radius: 5px;
      background-color: #01dcff;
    }

    .desktop-state {
      position: absolute;
      width: 100%;
      height: 100%;
      top: 0;
      left: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      user-select: none;
      background-color: rgba(0,0,0,0.4);
    

      .viewmode-control {
        width: 90px;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
    }

    .desktop-screen {
      cursor: pointer;
      background-color: black;
      width: 302px;
      height: 169px;
    }

    .desktop-controls {
      padding-top: 10px;
    }
  }
  .fullscreen {
    .desktop-screen {
      width: 100%;
      height: 100%;
    }
    .desktop-wrap {
      width: 100%;
      height: 100%;
    }
    .desktop-state{
      display: none;
    }
    .desktop-on-control{
      display: block;
    }
  }
</style>