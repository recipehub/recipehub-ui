(function(){
    angular.module('recipehub')
        .controller('PageController', ['$location', '$scope', 'SearchService', function pageController($location, $scope, $searchService) {
            $scope.go = function (path, search) {
                if (!search) {
                    $location.search({q:null});
                    $location.search({fork:null});
                    // $location.search({q:''});
                    // $location.search({fork:''});
                }
                $location.path(path);
                if (search) {
                    $location.search(search);
                }
            };

            $scope.fireSearch = function () {
                $scope.go('/search', {q: $scope.searchQuery})
            };

            $scope.myRecipes = function () {
                $scope.go('/myrecipes')
            };

        }]);


})();
