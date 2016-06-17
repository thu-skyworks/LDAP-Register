var App = angular.module('App', ['ngResource', 'ngCookies']);

App.factory('ErrNotify', function () {
    var errList = ['成功', '错误的参数', '没有这个用户', '密码错误',
        '用户没有登录', '用户或邮箱已存在', '会话过期', '没有绑定', '账号绑定过期',
        '用户没有发过状态', '对方没有开通本应用', '密码过短或过长',
        '第三方API错误', '操作超时', '清语API错误',
        '至少绑定一个账号'];
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


App.controller('root-controller', function ($scope,$http,ErrNotify) {
    $scope.tabClick = function(tab) {
        $scope.currentTab=tab;
    };
    $scope.register = function(){
        var err=0;
        $scope.tip_email=($scope.email===''?(err=1,'不能为空'):'');
        $scope.tip_passwd=($scope.passwd===''?(err=1,'不能为空'):'');
        $scope.tip_userid=($scope.userid===''?(err=1,'不能为空'):'');
        $scope.tip_realname=($scope.realname===''?(err=1,'不能为空'):'');
        $scope.error_tip_reg='';
        if(err)
            return;
        $http.post('user/reg',
            $.param({
                    email: $scope.email, 
                    userid: $scope.userid,
                    passwd: $scope.passwd,
                    realname: $scope.realname,
                }),
                {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}
            )
            .success(function (result) {
                if (result.error) {
                    $scope.error_tip_reg = ErrNotify.strError(result.error)
                    return;
                }else{
                    alert('注册成功！')
                }
                
            });
    };
    $scope.verify_email = function(){
        $scope.error_tip = '此功能暂不开放';
    }
    $scope.email='';
    $scope.userid='';
    $scope.passwd='';
    $scope.realname='';
    $scope.currentTab=0;
    $scope.reset_step=1;
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

