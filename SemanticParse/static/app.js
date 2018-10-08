myApp.config(function($routeProvider) {
   $routeProvider
       .when('/', { templateUrl: 'static/view/home.html'})
       .when('/login', {
          templateUrl: 'static/view/login.html',
           controller: 'loginController'
       })
       .when('/logout', {
          controller: 'logoutController'
       })
       .when('/register', {
          templateUrl: 'static/view/register.html',
          controller: 'registerController'
       })
       .otherwise({
           redirectTo: '/'
       });
});

//restricted router app
myApp.run(function ($rootScope, $location, $route, AuthService) {
   $rootScope.$on('$routeChangeStart', function(event, next, current) {
      if(next.access.restricted && AuthService.isLoggedIn() === false) {
         $location.path('/login');
         $route.reload();
      }
   })
});