/*
需要抓取的信息比较多，抓随申办的包，需要进入
1、随申码界面
2、核酸记录页面，加载更多页面
就能抓到下面所有的请求，把自己的header和body贴入即可。
*/ 

const inputValue = "1";
const theme_colors = {
    green: ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"],
    blue: ["#ebedf0", "#79B8FE", "#2188FF", "#005CC5", "#044289"]
}


if (inputValue) {
    // let username = inputValue.split(",")[0]
    let theme = inputValue.split(",")[1] ? theme_colors[inputValue.split(",")[1]] : theme_colors.green

    // 用默认logo替换头像
    let logo = "https://wx.qlogo.cn/mmhead/Q3auHgzwzM76niaZYsWjwHial7D9wvGqOwlL8F9BYLOicicTTuPOAibN4Xw/0"


    // 抓取mw，用于获取核酸记录的授权信息
    let resp_mw = await await $http.post({
        url: "https://smartgate.ywtbsupappw.sh.gov.cn/ebus/swift/mw/v1",
        header: {
            //这里需要替换自己的
            "Connection": "keep-alive",
            "X-Tif-Did": "nHSmNxA0d4",
            "X-Tif-Sid": "330ae4d073b13f3dcd62",
            "Content-Type": "application/json",
            "Authentication": "35361c848ad548b2954c60e711b7aff6",
            "Token": "13a589cd26c6980b7a3b76555f4d9125368603f31b34b202cbfbf8b9415fffc1beae85a13b800808785042a62ceceb340634a671c5209c3fb96176f62681e004df598d5bfd7a676c3939aca7287f8c72691fa45f6fff5a7dff285f0f88fc77f7bd8b8209832ff82a24e30dff41c4ebd3e86ebd110c0cd0fec5a327d24523a2bb",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.22(0x18001628) NetType/WIFI Language/zh_CN",
            "Referer": "https://servicewechat.com/wxc5059c3803665d9c/456/page-frame.html",
            "Accept-Encoding": "gzip",
        },
        body: {"params":{},"userSystemData":{"brand":"iPhone","model":"iPhone 12 Pro Max<iPhone13,4>","version":"8.0.22","system":"iOS 16.0","platform":"ios","SDKVersion":"2.24.5","windowWidth":428},"sessionId":"35361c848ad548b2954c60e711b7aff9"}
      });

    let mw = resp_mw.data.data

    // 抓取第一页的核酸记录
    let resp_hs = await await $http.post({
        url: "https://suishenmaback2.sh.gov.cn/smzy/shspace/hs/getByMwV3",
        header: {
            //这里需要替换自己的
            'Host': 'suishenmaback2.sh.gov.cn',
			'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryLYZBL1SQiWEH4HiB',
			'Origin': 'https://suishenmaback2.sh.gov.cn',
			'Accept-Encoding': 'gzip, deflate, br',
			'Connection': 'keep-alive',
			'Accept': 'application/json, text/plain, */*',
			'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.22(0x18001628) NetType/WIFI Language/zh_CN',
			'Referer': 'https://suishenmaback2.sh.gov.cn/smzy/h5/preventionV2?from=wx&mw=MSpMNMFzg3OiT96RONyNI7Lcti8tl7nb6saysLjzEzRlBtrxdx0rhXc%2Flrij5vaSnfmxBU31T3XsK54c6BNflquMrvb%2Fsx2GQDzxDWwpLys1rp%2F%20CaLpiao70kYJlfhro%2FxXQeZyyQfKCu4KVXdWYw%3D%3D&latitude=31.22390126575324&longitude=121.52603880715792&_t=1654763159747',
			'Content-Length': '293',
			'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        },
        form: {"mw":mw},
      });

    let data_hs = resp_hs.data.data
    let data_hs_sessionId = resp_hs.data.sessionId


      // 抓取第二页的核酸记录，sessionId 从第一页的返回里获取
    let resp_hs_2 = await await $http.post({
        url: "https://suishenmaback2.sh.gov.cn/smzy/shspace/hs/getHistory",
        header: {
            //这里需要替换自己的
            'Host': 'suishenmaback2.sh.gov.cn',
			'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryIHmc7eeacCQul3df',
			'Origin': 'https://suishenmaback2.sh.gov.cn',
			'Accept-Encoding': 'gzip, deflate, br',
			'Cookie': 'WT-group10-3=ac1e7d2c8bf9122c5250; WT-group10=BnOQDgjgEqzoakQWA75mVQ$$',
			'Connection': 'keep-alive',
			'Accept': 'application/json, text/plain, */*',
			'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.22(0x18001628) NetType/WIFI Language/zh_CN',
			'Referer': 'https://suishenmaback2.sh.gov.cn/smzy/h5/preventionV2?from=wx&mw=MSpMNMFzg3OiT96RONyNI7Lcti8tl7nb6saysLjzEzRlBtrxdx0rhXc%2Flrij5vaSnfmxBU31T3XsK54c6BNflquMrvb%2Fsx2GQDzxDWwpLys1rp%2F%20CaLpiao70kYJlfhro%2FxXQeZyyQfKCu4KVXdWYw%3D%3D&latitude=31.22390126575324&longitude=121.52603880715792&_t=1654763159747',
			'Content-Length': '425',
			'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        },
        form: {"sessionId":data_hs_sessionId},
      });

    let data_hs_2 = resp_hs_2.data.data

      // 抓取随申码的头像，不过太丑了，最后没用
    let resp_avatar = await await $http.post({
        url: "https://smartgate.ywtbsupappw.sh.gov.cn/ebus/suishenma/unified/photo/v3",
        header: {
             //这里需要替换自己的
        },
        body: {
             //这里需要替换自己的
        }
      });
    let avatar = resp_avatar.data.data.img

    // 抓取随申码的姓名，注意隐私的也可以不用
    let resp_username =await $http.post({
        url: "https://smartgate.ywtbsupappw.sh.gov.cn/ebus/suishenma/epidemicPrevention/getNucleicAcidTest",
        header: {
            //这里需要替换自己的
        },
        body: {
             //这里需要替换自己的
        }
      });

    let username = resp_username.data.data.name
    
    let data_all = data_hs.concat(data_hs_2)  // 合并两页核算记录
    let color_data = data2array(data_all)  // 转换成颜色值

    $widget.setTimeline({
        render: ctx => {
            //$widget.family = 1
            const family = ctx.family;
            const width = $widget.displaySize.width
            const height = $widget.displaySize.height

            let colors_row_spacing = 2 
            let colors_column_spacing = 4 

            colors_data=color_data
            let colors_view = []
            let colors_square_width = family == 0 ? (width - 30 - 8 * colors_row_spacing) / 9 : (width - 30 - 19 * colors_row_spacing) / 20
            
            for (var i = 0; i < colors_data.length; i++) {
                colors_view.push({
                    type: "color",
                    props: {
                        light: theme[colors_data[i]],
                        dark: colors_data[i] == "0" ? "#3E3E41" : theme[colors_data[i]],
                        frame: {
                            width: colors_square_width,
                            height: colors_square_width
                        },
                        cornerRadius: 2
                    }
                })
            }

            return {
                type: "vstack",
                props: {
                    alignment: $widget.horizontalAlignment.leading,
                    spacing: 10,
                    frame: {
                        width: width - 30,
                        height: height
                    },
                    // widgetURL: url
                },
                views: [
                    {
                        type: "hstack",
                        props: {
                            alignment: $widget.verticalAlignment.center,
                            spacing: 3
                        },
                        views: [
                            {
                                type: "image",
                                props: {
                                    
                                    // image: $image("data:image/png;base64,"+avatar),
                                    uri: logo,    // 这里用默认logo，如果要用自己的头像，用上一行。
                                    frame: {
                                        width: 20,
                                        height: 20
                                    },
                                    cornerRadius: {
                                        value: 10,
                                        style: 0
                                    },
                                    resizable: true
                                }
                            },
                            {
                                type: "text",
                                props: {
                                    text: "@"+username,
                                    font: $font("bold", 13),
                                    color: $color("#9A9AA1"),
                                    minimumScaleFactor: 0.5,
                                    lineLimit: 1
                                }
                            },
                            
                        ]
                    },
                    {
                        type: "hgrid",
                        props: {
                            rows: Array(7).fill({
                                flexible: {
                                    minimum: 10,
                                    maximum: Infinity
                                },
                                spacing: colors_column_spacing
                            }),
                            spacing: colors_row_spacing
                        },
                        views: colors_view
                    }
                ]
            }
        }
    })
}



// 转换日期到网格，瞎写的

function data2array(arr) {

    const now = new Date()
    const nowTime = now.getTime()
    const day = now.getDay()
    const oneDayTime = 24 * 60 * 60 * 1000
  
    const FirstTime = nowTime - (day - 1) * oneDayTime-56 * oneDayTime
    const monday = new Date(FirstTime)
    
    is_has =[]

    for (var i = 0; i < arr.length; i++) {
        let report_date = new Date(arr[i].report_date.replace(/-/g,"/"))
        let date = dateFormat("yyyy-mm-dd",report_date)
        is_has.push(date)
    }

    let output = []
    for (var i = 0; i < day+56; i++) {
        x = new Date( monday.setDate(monday.getDate()+1));
        y  = dateFormat("yyyy-mm-dd",x)
        let inc = is_has.includes(y)
        if (inc === true) {
            output.push(2)
        }else{
            output.push(0)
        }
    }
    return output
}


// 日期格式转换，百度复制粘贴的
function dateFormat(fmt, date) {
    let ret;
    const opt = {
        "y+": date.getFullYear().toString(),        // 年
        "m+": (date.getMonth() + 1).toString(),     // 月
        "d+": date.getDate().toString(),            // 日
        "H+": date.getHours().toString(),           // 时
        "M+": date.getMinutes().toString(),         // 分
        "S+": date.getSeconds().toString()          // 秒
        
    };
    for (let k in opt) {
        ret = new RegExp("(" + k + ")").exec(fmt);
        if (ret) {
            fmt = fmt.replace(ret[1], (ret[1].length == 1) ? (opt[k]) : (opt[k].padStart(ret[1].length, "0")))
        };
    };
    return fmt;
}
