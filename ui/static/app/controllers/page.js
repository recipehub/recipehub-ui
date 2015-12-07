(function(){
    angular.module('recipehub')
        .controller('PageController', ['$location', '$scope', function pageController($location, $scope) {
           $scope.go = function (path) {
                $location.path(path);
            };
        }]);

})();
