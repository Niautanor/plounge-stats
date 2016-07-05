angular.module('statsApp', ['ngRoute'])
    .controller('statsController', ['$scope', '$location', function($scope,$location) {
        $scope.isActive = function(viewLocation) {
            return viewLocation === $location.path();
        }
    }])
    .config(function($routeProvider, $locationProvider) {
        $routeProvider
            .when('/week', {
                templateUrl: 'tables/statsWeek.html'
            })
            .when('/day', {
                templateUrl: 'tables/statsDay.html'
            })
            .when('/weekS', {
                templateUrl: 'tables/statsWeekS.html'
            })
            .when('/dayS', {
                templateUrl: 'tables/statsDayS.html'
            })
            .when('/bees-all', {
                templateUrl: 'tables/beesAll.html'
            })
            .when('/bees-recent', {
                templateUrl: 'tables/beesRecent.html'
            })
            .when('/bees-week', {
                templateUrl: 'tables/beesWeek.html'
            })
            .when('/other-subreddits', {
                templateUrl: 'tables/otherSubreddits.html'
            })
            .when('/;-;', {
                templateUrl: 'tables/;-;.html'
            })
            .otherwise('/week');
    });
