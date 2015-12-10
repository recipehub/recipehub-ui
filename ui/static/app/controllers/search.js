(function(){
    angular.module('recipehub')
        .controller('SearchController', ['SearchService', '$scope', '$routeParams', function searchController($searchService, $scope, $routeParams) {

            var recipeId = $routeParams.id;
            var scope = $scope;

            $searchService.search($routeParams.q)
                .then(function(response) {
                    $scope.recipes = JSON.parse(response.data);
                });

        }]);

})();

