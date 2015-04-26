angular.module('statsApp', ['ngRoute'])
    .controller('statsController', ['$scope', '$location', function($scope,$location) {
        $scope.last_updated_file = 'stats/lastUpdated.txt';
        $scope.isActive = function(viewLocation) {
            return viewLocation === $location.path();
        }
    }])
    .config(function($routeProvider, $locationProvider) {
        $routeProvider
            .when('/week', {
                templateUrl: 'stats/statsWeek.txt'
            })
            .when('/day', {
                templateUrl: 'stats/statsDay.txt'
            })
            .when('/weekS', {
                templateUrl: 'stats/statsWeekS.txt'
            })
            .when('/dayS', {
                templateUrl: 'stats/statsDayS.txt'
            })
            .otherwise('/week');
    });
