//for controller module

//loginController
angular.module('myApp').controller('loginController',
    ['$scope', $location, 'AuthService',
    function($scope, $location, AuthService) {
        console.log("loginController");
        $scope.login = function() {
            $scope.error = false;
            $scoper.disabled = true;

            //call login from service
            AuthService.login($scope.loginForm.email, $scope.loginForm.password)
            //handle success
                .then(function() {
                    $location.path('/');
                    $scope.disabled = false;
                    $scope.loginForm = {};
                })
            //handle error
                .catch(function() {
                    $scope.error = true;
                    $scope.errorMessage = 'Invalid username and/or password';
                    $scope.disabled = false;
                    $scope.loginForm = {};
                });
        };
    }]);

//logout controller
angular.module('myApp').controller('logoutController',
    ['$scope', '$location', 'AuthService',
        function ($scope, $location, AuthService) {
            console.log("logout controller");
            $scope.logout = function () {
                //call logout from service
                AuthService.logout()
                    .then(function () {
                        $location.path('/login');
                    });

            };
        }]);

//register controller
angular.module('myApp').controller('registerController',
    ['$scope', '$location', 'AuthService',
    function ($scope, $location, AuthService) {
        console.log("register controller");
        $scope.register = function() {
            //initial values
            $scope.error = false;
            $scope.disabled = true;

            //call register from service
            AuthService.register($scope.registerForm.email,
                                $scope.registerForm.password)
            //handle success
                .then(function() {
                    $location.path('/login');
                    $scope.disabled = false;
                    $scope.registerForm = {};
                })
            //handle error
                .catch(function() {
                    $scope.error = true;
                    $scope.errorMessage = 'Something wrong!';
                    $scope.disabled = false;
                    $scope.registerForm = {};
                });
        };
    }]);