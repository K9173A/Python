"""
Название: Порязрядная сортировка по наименьшей значащей цифре.
Автор: Harold H. Seward.
Год: 1954.
Класс Сортировки распределением.
Устойчивость: Нет.
Алгоритмическая сложность:
k - это значение количества бит, необходимых для кодирования самого большого
    числа (radix в алгоритме).
n - это длина списка с исходными данными.
1. Худший случай: O(k * n)
2. Средний случай: O(k * n).
3. Лучший случай: O(n).
"""
import math


def calculate_bucket_key(seq, radix, exp, min_element, index):
    """
    Вычисляет индекс корзины для данного числа.
    :param seq: коллекция чисел.
    :param radix: основа системы счисления (обычно равна 10).
    :param exp: разряд цифры в числе (10, 100, 1000).
    :param min_element: минимальное число в коллекции.
    :param index: индекс числа из коллекции, для которого будет вычисляться
    значение.
    :return: индекс корзины для данного числа.
    """
    return math.floor(((seq[index] - min_element) / exp) % radix)


def counting_sort(seq, radix, exp, min_element):
    """
    Осуществляет сортировку для указанного разряда exp у чисел из seq.
    :param seq: коллекция чисел.
    :param radix: основа системы счисления (обычно равна 10).
    :param exp: разряд цифры в числе (10, 100, 1000).
    :param min_element: минимальное число в коллекции.
    :return: список с отсортированными по возрастанию элементами.
    """
    # Каждая ячеейка - это корзина для цифр, которые определяются индексом i.
    # Изначально заполняем список нулями, так это начальная частота появления
    # дл данного индекса i.
    buckets = [0] * radix
    seq_length = len(seq)
    # Список для результата, в котором будут уже отсортированные числа для
    # данной итерации (для данного exp - разряд числа).
    output = [None] * seq_length

    # На данном этапе высчитывается частота появления остатков в числах
    # коллекции. Все величины распределяются по корзинам, где индексом
    # является цифра, возвращённая calculate_bucket_key(), а значением -
    # частота повторения данного числа. Так как это версия LSD, то есть
    # начинается с наименее значащего разряда, exp принимает значения:
    # 1, 10, 100 и т.д. Таким образом при каждом последующем вызове функции
    # counting_sort() значение exp будет смещать разряд влево. Например:
    # если дано число 842, то будет анализироваться вначале 2, потом 4,
    # а затем 8.
    for i in range(seq_length):
        index = calculate_bucket_key(seq, radix, exp, min_element, i)
        buckets[index] += 1

    # К данному этапу у нас есть:
    # 1) Индексы i в buckets, которые являются всеми возможными числами
    #    доступными в системе с основанием radix.
    # 2) Значения частот, которые определяют количество повторяющихся цифр
    #    (индексов i) в массиве.
    # На данном этапе суммируются значения частот корзин. Учитывая, что
    # мы итерируемся по корзинам, то здесь будет "кумулятивный" эффект - то
    # есть каждое последующее значение будет собирать значения предыдущих -
    # все значения будут расположены по возрастанию в конечном счёте. Сумма
    # всех предыдущих значений нужна, чтобы определить, с какого индекса бу-
    # дет начинаться блок из этих чисел. Например:
    # 1) Есть два нуля.
    # 2) Есть пять единиц.
    # 3) Есть три двойки.
    # Тогда ячейка, в которой начнутся двойки в отсортированном массиве будут
    # определяться в виде суммы частот предыдущих корзин. 2 + 5 = 7 Значит с
    # седьмого индекса будет начинаться блок из двоек.
    for i in range(1, radix):
        buckets[i] += buckets[i - 1]

    for i in range(seq_length - 1, -1, -1):
        # Берём всё те же индексы, что мы брали и на первом этапе.
        index = calculate_bucket_key(seq, radix, exp, min_element, i)
        # Из частоты появления каждой цифры вычитаем единицу, так как на каж-
        # дой итерации данного этапа ровно одна цифра записывается в output.
        # Декрементом мы обозначаем, что 1 позиция уже использована.
        buckets[index] -= 1
        # Запись в целевой список. Индексом в output будет являться то, что мы
        # посчитали на этапе 2 - позиция числа уже в отсортированном списке.
        # значением будет число из исходного списка seq.
        output[buckets[index]] = seq[i]

    return output


def radix_sort(seq, radix=10):
    """
    Реализация поразрядной сортировки по наименьшей значащяей цифре.
    :param seq: любая изменяемая коллекция с числами.
    :param radix: основание системы счисления.
    :return: коллекция с элементами, расположенными по возрастанию.
    """
    # Случай с коллекциями длиной в 1 или 0 не имеет смысл обрабатывать.
    if len(seq) in [0, 1]:
        return seq

    min_element = min(seq)
    max_element = max(seq)
    exp = 1

    # Осуществояет поразрядную сортировку, начиная с наименьшего разряда.
    while (max_element - min_element) / exp >= 1:
        # Сортируем нужный разряд у чисел из seq.
        seq = counting_sort(seq, radix, exp, min_element)
        # Смещаемся на более старший разряд.
        exp *= radix

    return seq


if __name__ == '__main__':
    # user_input = input('Enter numbers separated by a comma:\n').strip()
    # unsorted = [int(item) for item in user_input.split(',')]
    unsorted = [55, 1, 4, 23, 53, 39, 42, 49, 12, 40, 74, 72]
    print(*radix_sort(unsorted), sep=',')
