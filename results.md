# Comparator Results

- AI samples: 1000 (tum-nlp/IDMGSP label=1, GPT-3 generated, abstract+intro+conclusion)
- Human samples: 1000 (allenai/peS2o v2, pre-2020)

| measure name                 |   AI papers |   human papers |        diff | AI or human   |
|------------------------------|-------------|----------------|-------------|---------------|
| semicolonFreq                |   0.0924032 |     0.128235   |  0.0358313  | human         |
| commaFreq                    |   4.40826   |     3.2895     |  1.11876    | AI            |
| emmdashFreq                  |   0         |     0.0215595  |  0.0215595  | human         |
| ellipsisFreq                 |   0.0072    |     0.00259524 |  0.00460476 | AI            |
| exclamationFreq              |   0.0120333 |     0.00278333 |  0.00925    | AI            |
| colonFreq                    |   0.174566  |     0.254208   |  0.0796423  | human         |
| parenthesesFreq              |   1.83926   |     2.16781    |  0.328548   | human         |
| sentences_starter_pronouns   |  13.9578    |     4.01013    |  9.94772    | AI            |
| sentences_starter_discourse  |   2.78202   |     2.2465     |  0.535517   | AI            |
| sentences_starter_and        |   0.313137  |     0.717833   |  0.404696   | human         |
| sentences_starter_but        |   0.124574  |     0.234879   |  0.110305   | human         |
| sentences_starter_i          |   0.0513028 |     0.208179   |  0.156876   | human         |
| sentences_starter_the        |  22.7411    |    15.9094     |  6.83175    | AI            |
| sentences_structure_avg      |  19.7383    |    22.4886     |  2.75028    | human         |
| sentences_structure_variance |   9.61057   |    10.1167     |  0.506129   | human         |
| sentences_structure_std_dev  |   9.61057   |    10.1167     |  0.506129   | human         |
| sentences_structure_long     |   2.911     |     8.80435    |  5.89335    | human         |
| sentences_structure_short    |   8.54084   |     8.49475    |  0.0460943  | AI            |
| filler_word_rate             |   0.244848  |     0.261613   |  0.016765   | human         |
| discourse_marker_rate        |   0.173997  |     0.132099   |  0.0418978  | AI            |
| type_token_ratio             |   0.334903  |     0.579181   |  0.244279   | human         |
| avg_word_length              |   5.04183   |     5.54237    |  0.500547   | human         |
