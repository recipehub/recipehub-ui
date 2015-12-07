(function(){
    angular.module('recipehub')
        .controller('RecipeController', ['RecipeService', '$scope', '$routeParams', function recipeController($recipeService, $scope, $routeParams) {
            $recipeService.getRecipe($routeParams.id)
                .then(function(response) {
                    $scope.recipe = response.data;
                    console.log(response.data)
                });
            $scope.modelArray = [1, 2, 3, 4]
        }]);
})();
