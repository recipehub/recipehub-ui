(function(){
    angular.module('recipehub')
        .controller('MyRecipesController', ['RecipeService', 'UserService', '$scope', '$routeParams', function searchController($recipeService, $userService, $scope, $routeParams) {

            var recipeId = $routeParams.id;
            var scope = $scope;

            $userService.getCurrentUser()
                .then(function(response) {
                    $recipeService.getUserRecipes(response.data.id)
                        .then(function(response) {
                            $scope.recipes = response.data;
                        });
                });
        }]);

})();
