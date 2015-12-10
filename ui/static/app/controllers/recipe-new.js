(function() {
    angular.module('recipehub')
        .controller('NewRecipeController', ['RecipeService', '$scope', '$routeParams', 'CommentService', 'RatingService', '$mdDialog', 'IngredientService', function recipeController($recipeService, $scope, $routeParams, $commentService, $ratingService, $mdDialog, $ingredientService) {

            var recipe = {
                ingredients: [{}, {}],
                steps: ['']
            };
            this.selectedIngredient = {};
            $scope.recipe = recipe;
            $scope.steps = 
            $scope.steps = [];
            var scope = $scope;
            $scope.newStep = ''

            $scope.results = {}

            $ingredientService.getIngredients()
                .then(function (response) {
                    $scope.AllIngredients = response.data;
                });


            $scope.querySearch = function (query) {
                var results = query ? $scope.AllIngredients.filter( createFilterFor(query) ) : $scope.AllIngredients;
                return results;
            };
            $scope.addMoreIngredients = function () {
                recipe.ingredients.unshift({});
            };

            $scope.addStep = function () {
                $scope.steps.push($scope.newStep);

            };

            $scope.save = function () {
                var finalIngredients = {}
                for (key in $scope.recipe.ingredients) {
                    if ($scope.recipe.ingredients[key].selected) {
                        finalIngredients[$scope.recipe.ingredients[key].selected.id] = parseInt($scope.recipe.ingredients[key].amount)
                    }
                }
                console.log(finalIngredients)
                var to_save = {
                    'title': recipe['title'],
                    'description': recipe['description'],
                    'ingredients': finalIngredients,
                    'steps': $scope.steps
                }
                $recipeService.newRecipe(to_save)
            };



            function createFilterFor(query) {
                var lowercaseQuery = angular.lowercase(query);

                return function filterFn(ingredient) {
                    return (angular.lowercase(ingredient.name).indexOf(lowercaseQuery) === 0);
                };

            }
        }]);

})();

