angular.module('statsApp', ['ngRoute'])
    .controller('statsController', ['$scope', '$location', function($scope,$location) {
        $scope.isActive = function(viewLocation) {
            return viewLocation === $location.path();
        }
    }])
    .config(function($routeProvider, $locationProvider) {
        $routeProvider
            .when('/week', {
                templateUrl: 'stats_files/statsWeek.txt'
            })
            .when('/day', {
                templateUrl: 'stats_files/statsDay.txt'
            })
            .when('/weekS', {
                templateUrl: 'stats_files/statsWeekS.txt'
            })
            .when('/dayS', {
                templateUrl: 'stats_files/statsDayS.txt'
            })
            .otherwise('/week');
    });
