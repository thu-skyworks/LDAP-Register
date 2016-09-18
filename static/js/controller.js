var App = angular.module('App', ['ngResource', 'ngCookies']);

App.factory('ErrNotify', function () {
    var errList = ['成功', '错误的参数', '没有这个用户', '密码错误',
        '用户没有登录', '用户或邮箱已存在', '会话过期', '没有绑定', '账号绑定过期',
        '用户没有发过状态', '对方没有开通本应用', '密码过短或过长',
        '第三方API错误', '操作超时', '清语API错误',
        '至少绑定一个账号', '没有使用权限', '解析错误', '操作进行中', '无效的验证码'];
    errList[-1] = '未知错误';
    function showError(str) {
        showMessage(str, 'error');
    }

    function strError(code) {
        if (errList[code])
            return errList[code];
        else
            return "错误代码：" + code
    }

    return {
        handleError: function (data) {
            if (!data || data.error) {
                var str = strError(data && data.error);
                showError(str);
                return true
            }
            return false
        },
        strError: strError,
        showError: showError
    }
});


App.controller('root-controller', function ($scope,$http,$location,ErrNotify) {
    $scope.tabClick = function(tab) {
        $scope.currentTab=tab;
    };
    $scope.register = function(){
        var err=0;
        var regemail=(($scope.regemail||'').trim());
        var userid=(($scope.userid||'').trim());
        var realname=(($scope.realname||'').trim());
        var regpasswd = ($scope.regpasswd||'');
        $scope.tip_regemail=(!validateEmail(regemail)?(err=1,'无效的邮箱'):'');
        $scope.tip_userid=(userid===''?
                (err=1,'不能为空'):
                (/^\w+$/.test(userid) ? '': (err=1,'仅允许字母数字'))
            );
        $scope.tip_regpasswd=(regpasswd===''?(err=1,'不能为空'):'');
        $scope.tip_realname=(realname===''?(err=1,'不能为空'):'');
        $scope.error_tip_reg='';
        if(err)
            return;
        $http.post('user/reg',
            $.param({
                    email: regemail, 
                    userid: userid,
                    passwd: regpasswd,
                    realname: realname,
                }),
                {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}
            )
            .success(function (result) {
                if (result.error) {
                    $scope.error_tip_reg = ErrNotify.strError(result.error)
                    return;
                }else{
                    alert('注册成功！您可以开始使用wiki、nas等业务了。');
                    location.href = '/';
                }
                
            });
    };
    $scope.reset1 = function(){
        var err=0;
        $scope.tip_email=($scope.email===''?(err=1,'不能为空'):'');
        $scope.error_tip='';
        if(err)
            return;
        $http.post('user/reset1',
            $.param({
                    email: $scope.email, 
                }),
                {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}
            )
            .success(function (result) {
                if (result.error) {
                    $scope.error_tip = ErrNotify.strError(result.error)
                    return;
                }else{
                    alert('密码重置邮件已发送，请根据邮件内容操作！（未收到请检查垃圾邮件）');
                    location.href = '/';
                }
            });

    }
    $scope.set_passwd = function(){
        var err=0;
        $scope.tip_passwd=($scope.passwd===''?(err=1,'不能为空'):'');
        if($scope.reppasswd === ''){
            err = 1;
            $scope.tip_reppasswd = '不能为空';
        }else if($scope.reppasswd!==$scope.passwd){
            err = 1;
            $scope.tip_reppasswd = '输入不相同';
        }else{
            $scope.tip_reppasswd = '';
        }
        $scope.error_tip='';
        if(err)
            return;
        $http.post('user/reset2',
            $.param({
                    passwd: $scope.passwd, 
                    code: $location.search()['code']
                }),
                {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}
            )
            .success(function (result) {
                if (result.error) {
                    $scope.error_tip = ErrNotify.strError(result.error)
                    return;
                }else{
                    alert('密码重置成功');
                    location.href = '/';
                }
            });

    }
    $scope.email='';
    $scope.userid='';
    $scope.passwd='';
    $scope.realname='';
    $scope.currentTab=({'/reg':0, '/reset':1})[$location.path()] || 0;
    $scope.reset_step=$location.search()['reset_step2'] ? 2 : 1;
});
App.directive('errSrc', function () {
    return {
        link: function (scope, element, attrs) {
            element.bind('error', function () {
                if (attrs.src != attrs.errSrc) {
                    attrs.$set('src', attrs.errSrc);
                }
            });
        }
    }
});
App.filter('slice', function() {
  return function(arr, start, end) {
    return (arr || []).slice(start, end);
  };
});

function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}
