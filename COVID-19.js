// 别人框架抄过来的，可以加配置信息，懒得改了
const inputValue = "1"

if (inputValue) {
    let resp =await $http.post({
        url: "https://smartgate.ywtbsupappw.sh.gov.cn/ebus/suishenma/epidemicPrevention/getNucleicAcidTest",

        // header 需要使用微信的随申办抓包，目测"X-Tif-Did"、"X-Tif-Sid"、"Token"、"Authentication" 都是需要的
        header: {
            "Connection": "keep-alive",
            "X-Tif-Did": "nHSmNxA0d4",
            "X-Tif-Sid": "330ae4d073b13f3dcd60",
            "Content-Type": "application/json",
            "Authentication": "35361c848ad548b2954c60e711b7aff9",
            "Token": "13a589cd26c6980b7a3b76555f4d9140368603f31b34b202cbfbf8b9415fffc1beae85a13b800808785042a62ceceb340634a671c5209c3fb96176f62681e004df598d5bfd7a676c3939aca7287f8c72691fa45f6fff5a7dff285f0f88fc77f7bd8b8209832ff82a24e30dff41c4ebd3e86ebd110c0cd0fec5a327d24523a2bb",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.22(0x18001628) NetType/WIFI Language/zh_CN",
            "Referer": "https://servicewechat.com/wxc5059c3803665d9c/456/page-frame.html",
            "Accept-Encoding": "gzip",
        },
        //后面有个sessionId，需要加一下？
        body: {"params":{},"userSystemData":{"brand":"iPhone","model":"iPhone 12 Pro Max<iPhone13,2>","version":"8.0.23","system":"iOS 15.5","platform":"ios","SDKVersion":"2.24.5","windowWidth":428},"sessionId":"35361c848ad548b2954c60e711b7aff9"}
      });

    let data = resp.data.data
    let username = data.name
    let sampleDate = data.sampleDate
    let title = data.collectModeName
    let logo = "https://wx.qlogo.cn/mmhead/Q3auHgzwzM76niaZYsWjwHial7D9wvGqOwlL8F9BYLOicicTTuPOAibN4Xw/0"


    let counters =[0,1]
    let counter_view = []
    let type_view = []

    const now = new Date();
    const sampleDate_datetime = new Date(sampleDate.replace(/-/g,"/"))    
    const expireDate = parseInt(72-(now.getTime()-sampleDate_datetime)/60/60/1000)

    // 本来想多放点数据的，发现没有，for也不改了
    for (var i in counters) {
        counter_view.push({
            type: "text",
            props: {
                text: expireDate.toString()+"h",
                font: $font("bold", 18),
                light: "#282828",
                dark: "white",
                minimumScaleFactor: 0.5,
                lineLimit: 1
            }
        })
        type_view.push({
            type: "text",
            props: {
                text: "72h倒计时",
                font: $font(10),
                color: $color("#aaaaaa"),
                minimumScaleFactor: 0.5,
                lineLimit: 1
            }
        })
    }

    $widget.setTimeline({
        render: ctx => {
            //$widget.family = 0
            const family = ctx.family;
            const width = $widget.displaySize.width
            const height = $widget.displaySize.height

            const logo_view = {
                type: "image",
                props: {
                    uri: logo,
                    frame: {
                        width: 60,
                        height: 60
                    },
                    resizable: true,
                    cornerRadius: 15
                }
            }

            const desc = {
                type: "text",
                props: {
                    text: "上次核酸",
                    font: $font(10),
                    color: $color("#aaaaaa"),
                    minimumScaleFactor: 0.5,
                    lineLimit: 1
                }
            }

            const title_view = {
                type: "text",
                props: {
                    text: title,
                    font: family == 0 ? $font("bold", 20) : $font("bold", 25),
                    light: "#282828",
                    dark: "white",
                    minimumScaleFactor: 0.5,
                    lineLimit: 1
                }
            }

            const path_view = {
                type: "text",
                props: {
                    text: "@" + sampleDate,
                    font: $font(10),
                    color: $color("#2481cc"),
                    minimumScaleFactor: 0.5,
                    lineLimit: 1
                }
            }

            const small_widget = [
                {
                    
                    type: "hstack",
                    props: {
                        
                        alignment: $widget.verticalAlignment.center,
                        frame: {
                            width: width - 30,
                            height: 60
                        },
                        spacing: 0
                    },
                    views: [
                        logo_view,
                        {
                            type: "vstack",
                            props: {
                            
                                
                                alignment: $widget.horizontalAlignment.center,
                                frame: {
                                    maxWidth: Infinity,
                                    maxHeight: Infinity
                                },
                                spacing: 0
                            },
                            views: [
                                counter_view.concat(type_view)[0],
                                counter_view.concat(type_view)[counter_view.concat(type_view).length / 2]
                            ]
                        }
                    ]
                },
                spacerMaker(10, width - 30),
                desc,
                spacerMaker(3, width - 30),
                title_view,
                spacerMaker(3, width - 30),
                path_view
            ]

            
            // blaunch ，是app store 需要安装「小捷径」才能跳转
            return {
                type: "vstack",
                props: {
                    
                    alignment: $widget.horizontalAlignment.leading,
                    frame: {
                        width: width - 30,
                        height: height
                    },

                    spacing: 0,
                    widgetURL: "blaunch://wx?id=gh_d4acc9de8978&path=pages/suishenma/jiankangma/index.html?needLogin=false&scene=0"
                    
                },
                views: small_widget
            }
        }
    })
}

function spacerMaker(height, width) {
    return {
        type: "spacer",

        props: {
            frame: {
                width: width,
                height: height
            }
        }
    }
}
