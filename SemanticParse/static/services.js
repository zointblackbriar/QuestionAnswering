angular.module('myApp').factory('AuthService',
    ['$q', '$timeout', '$http',
    function($q, $timeout, $http) {
    //create an user variable

        var user = null;

        //return available functions for use in controllers
        return({
            isLoggedIn : isLoggedIn,
            login : login,
            logout : logout,
            register : register,
            getUserStatus : getUserStatus
        });

        //Check whether the user is logged in or not
        function isLoggedIn(){
            if(user){
                return true;
            } else {
                return false;
            }
        }
        //login service
        function login(email, password){
            //create an instance of Promise
            var deferred = $q.defer();

            $http.post('/api/login', {email: email, password : password})
            //handle success
                .success(function(data, status) {
                    if(status == 200 && data.result) {
                        user = true;
                        deferred.resolved();
                    } else {
                        user = false;
                        deferred.reject();
                    }
                })
                //handle error
                .error(function(data) {
                    user = false;
                    deferred.reject();
                });

            return deferred.promise;
        }

        //register service
        function register(email, password) {
            //create a new instance of deferred

            var deferred = $q.defer();
            //send a post request to the server
            $http.post('/api/register', {email : email, password : password})
            //handle success
                .success(function(data, status) {
                    if(status === 200 && data.result) {
                        deferred.resolve();
                    } else {
                        deferred.reject();
                    }
                })
            //handle error
                .error(function(data) {
                    deferred.reject();
                });
        }

        //get status service
        function getUserStatus() {
            return $http.get('/api/status')
            //handle success
                .success(function (data) {
                    if(data.status) {
                        user = true;
                    } else {
                        user = false;
                    }
                })
            //handle error
                .error(function(data) {
                    user = false;
                });
            }
    }]);