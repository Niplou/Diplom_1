import pytest
from unittest.mock import Mock
from burger import Burger
from bun import Bun
from ingredient import Ingredient
from ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestBurger:

    # Тесты для метода set_buns
    def test_set_buns(self):
        burger = Burger()
        mock_bun = Mock(spec=Bun)
        
        burger.set_buns(mock_bun)
        
        assert burger.bun == mock_bun

    # Тесты для метода add_ingredient
    def test_add_ingredient(self):
        burger = Burger()
        mock_ingredient = Mock(spec=Ingredient)
        
        burger.add_ingredient(mock_ingredient)
        
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient

    # Тесты для метода remove_ingredient
    def test_remove_ingredient(self):
        burger = Burger()
        mock_ingredient1 = Mock(spec=Ingredient)
        mock_ingredient2 = Mock(spec=Ingredient)
        
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        
        burger.remove_ingredient(0)
        
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient2

    # Тесты для метода move_ingredient
    def test_move_ingredient(self):
        burger = Burger()
        mock_ingredient1 = Mock(spec=Ingredient)
        mock_ingredient2 = Mock(spec=Ingredient)
        mock_ingredient3 = Mock(spec=Ingredient)
        
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        burger.add_ingredient(mock_ingredient3)
        
        burger.move_ingredient(0, 2)
        
        assert burger.ingredients[0] == mock_ingredient2
        assert burger.ingredients[1] == mock_ingredient3
        assert burger.ingredients[2] == mock_ingredient1

    # Параметризованные тесты для метода get_price
    @pytest.mark.parametrize("bun_price,ingredient_prices,expected_total", [
        (100, [50, 75], 325),  # 100*2 + 50 + 75 = 325
        (50, [25, 30, 45], 200),  # 50*2 + 25 + 30 + 45 = 200
        (200, [], 400),  # 200*2 + 0 = 400
        (0, [10, 20], 30),  # 0*2 + 10 + 20 = 30
    ])
    def test_get_price_with_different_combinations(self, bun_price, ingredient_prices, expected_total):
        burger = Burger()
        
        # Мок булки
        mock_bun = Mock(spec=Bun)
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)
        
        # Моки ингредиентов
        for price in ingredient_prices:
            mock_ingredient = Mock(spec=Ingredient)
            mock_ingredient.get_price.return_value = price
            burger.add_ingredient(mock_ingredient)
        
        result = burger.get_price()
        
        assert result == expected_total
        mock_bun.get_price.assert_called_once()

    # Тест для метода get_price с проверкой вызовов методов
    def test_get_price_calls_methods(self):
        burger = Burger()
        
        mock_bun = Mock(spec=Bun)
        mock_bun.get_price.return_value = 100
        burger.set_buns(mock_bun)
        
        mock_ingredient1 = Mock(spec=Ingredient)
        mock_ingredient1.get_price.return_value = 50
        burger.add_ingredient(mock_ingredient1)
        
        mock_ingredient2 = Mock(spec=Ingredient)
        mock_ingredient2.get_price.return_value = 75
        burger.add_ingredient(mock_ingredient2)
        
        result = burger.get_price()
        
        assert result == 325  # 100*2 + 50 + 75
        mock_bun.get_price.assert_called_once()
        mock_ingredient1.get_price.assert_called_once()
        mock_ingredient2.get_price.assert_called_once()

    # Параметризованные тесты для метода get_receipt
    @pytest.mark.parametrize("bun_name,ingredients_data,expected_lines", [
        (
            "black bun", 
            [
                (INGREDIENT_TYPE_SAUCE, "hot sauce"),
                (INGREDIENT_TYPE_FILLING, "cutlet")
            ],
            [
                "(==== black bun ====)",
                "= sauce hot sauce =",
                "= filling cutlet =", 
                "(==== black bun ====)",
                "",  # Пустая строка после второй булки
                "Price: 0"
            ]
        ),
        (
            "white bun",
            [
                (INGREDIENT_TYPE_FILLING, "dinosaur"),
                (INGREDIENT_TYPE_SAUCE, "sour cream")
            ],
            [
                "(==== white bun ====)",
                "= filling dinosaur =",
                "= sauce sour cream =",
                "(==== white bun ====)", 
                "",  # Пустая строка после второй булки
                "Price: 0"
            ]
        ),
    ])
    def test_get_receipt_format(self, bun_name, ingredients_data, expected_lines):
        burger = Burger()
        
        # Мок булки
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = bun_name
        mock_bun.get_price.return_value = 0
        burger.set_buns(mock_bun)
        
        # Моки ингредиентов
        for ingredient_type, ingredient_name in ingredients_data:
            mock_ingredient = Mock(spec=Ingredient)
            mock_ingredient.get_type.return_value = ingredient_type
            mock_ingredient.get_name.return_value = ingredient_name
            mock_ingredient.get_price.return_value = 0
            burger.add_ingredient(mock_ingredient)
        
        receipt = burger.get_receipt()
        receipt_lines = receipt.split('\n')
        
        assert len(receipt_lines) == len(expected_lines)
        for i, expected_line in enumerate(expected_lines):
            assert receipt_lines[i] == expected_line

    # Тест для метода get_receipt с правильной ценой
    def test_get_receipt_with_price(self):
        burger = Burger()
        
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = "red bun"
        mock_bun.get_price.return_value = 100
        burger.set_buns(mock_bun)
        
        mock_ingredient = Mock(spec=Ingredient)
        mock_ingredient.get_type.return_value = INGREDIENT_TYPE_SAUCE
        mock_ingredient.get_name.return_value = "chili sauce"
        mock_ingredient.get_price.return_value = 50
        burger.add_ingredient(mock_ingredient)
        
        receipt = burger.get_receipt()
        
        assert "Price: 250" in receipt  # 100*2 + 50 = 250
        assert "(==== red bun ====)" in receipt
        assert "= sauce chili sauce =" in receipt

    # Тест для пустого бургера (только булки)
    def test_get_receipt_only_bun(self):
        burger = Burger()
        
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = "white bun"
        mock_bun.get_price.return_value = 200
        burger.set_buns(mock_bun)
        
        receipt = burger.get_receipt()
        receipt_lines = receipt.split('\n')
        
        expected_lines = [
            "(==== white bun ====)",
            "(==== white bun ====)",
            "",
            "Price: 400"
        ]
        
        assert len(receipt_lines) == len(expected_lines)
        for i, expected_line in enumerate(expected_lines):
            assert receipt_lines[i] == expected_line

    # Тест на удаление ингредиента с несуществующим индексом
    def test_remove_ingredient_invalid_index(self):
        burger = Burger()
        mock_ingredient = Mock(spec=Ingredient)
        burger.add_ingredient(mock_ingredient)
        
        # Должен поднять IndexError при попытке удалить несуществующий индекс
        with pytest.raises(IndexError):
            burger.remove_ingredient(5)

    # Тест на перемещение ингредиента с несуществующим индексом
    def test_move_ingredient_invalid_index(self):
        burger = Burger()
        mock_ingredient = Mock(spec=Ingredient)
        burger.add_ingredient(mock_ingredient)
        
        # Должен поднять IndexError при попытке переместить несуществующий индекс
        with pytest.raises(IndexError):
            burger.move_ingredient(5, 0)

    # Дополнительный тест для проверки преобразования типов ингредиентов в нижний регистр
    def test_get_receipt_ingredient_types_lowercase(self):
        burger = Burger()
        
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = "test bun"
        mock_bun.get_price.return_value = 0
        burger.set_buns(mock_bun)
        
        # Добавляем ингредиенты с разными типами
        mock_sauce = Mock(spec=Ingredient)
        mock_sauce.get_type.return_value = INGREDIENT_TYPE_SAUCE
        mock_sauce.get_name.return_value = "test sauce"
        mock_sauce.get_price.return_value = 0
        
        mock_filling = Mock(spec=Ingredient)
        mock_filling.get_type.return_value = INGREDIENT_TYPE_FILLING
        mock_filling.get_name.return_value = "test filling"
        mock_filling.get_price.return_value = 0
        
        burger.add_ingredient(mock_sauce)
        burger.add_ingredient(mock_filling)
        
        receipt = burger.get_receipt()
        
        # Проверяем, что типы ингредиентов преобразованы в нижний регистр
        assert "= sauce test sauce =" in receipt
        assert "= filling test filling =" in receipt