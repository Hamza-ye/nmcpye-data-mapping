# Mapping status

The following table shows NORTH/SOUTH Health Facilities that have some data in the north files and needs either be mapped to catchments localities or locate their GPS coordinate:

| **hf_owner** | **-** | **WITH NO CATCHMENTS** | **WITH NO CATCHMENT & GPS** | **WITH NO GPS** |
|--------------|:-----:|------------------------|-----------------------------|-----------------|
| **OTHER**    |  292  |                        |                             |                 |
| **PRIVATE**  |  574  |                        |                             |       111       |
| **PUBLIC**   |  4692 |          848           |             291             |        1        |

There are currently {--118234--} {++120982++} locations in total, of which {--105855: 89%--} {++110898: 91%++} have been mapped to a **health facility** in the `md_health_facilities.csv` master file.

| **S/N**     | **gov_id** | **gov**          |                 **%**                 | **MAPPED** | **UNMAPPED** |
|-------------|:----------:|------------------|:-------------------------------------:|:----------:|:------------:|
| NORTH       |     11     | Ibb              | ![100](https://geps.dev/progress/100) |    16497   |              |
| NORTH       |     17     | Hajjah           | ![100](https://geps.dev/progress/100) |    14416   |              |
| NORTH       |     20     | Dhamar           | ![100](https://geps.dev/progress/100) |    14219   |              |
| NORTH/SOUTH |     18     | Al Hudaydah      | ![100](https://geps.dev/progress/100) |    9508    |              |
| NORTH       |     23     | Sana'a           | ![100](https://geps.dev/progress/100) |    7504    |       1      |
| NORTH       |     22     | Sa'ada           | ![100](https://geps.dev/progress/100) |    6992    |              |
| NORTH       |     31     | Raymah           | ![100](https://geps.dev/progress/100) |    6766    |              |
| NORTH       |     29     | Amran            | ![100](https://geps.dev/progress/100) |    6421    |              |
| NORTH       |     16     | Al Jawf          | ![100](https://geps.dev/progress/100) |    2650    |              |
| NORTH       |     27     | Al Mahwit        | ![99.4](https://geps.dev/progress/99) |    4788    |      29      |
| NORTH/SOUTH |     26     | Marib            | ![91.1](https://geps.dev/progress/91) |    2181    |      213     |
| NORTH       |     13     | Amanat Al Asimah | ![88.1](https://geps.dev/progress/88) |    5736    |      773     |
| NORTH/SOUTH |     15     | Taizz            | ![51.4](https://geps.dev/progress/51) |    9574    |     9068     |
| NORTH/SOUTH |     14     | Al Bayda         | ![100](https://geps.dev/progress/100) |    3646    |              |

### Join status between reports and catchments

### ITNs Reports `rd_itns_data.csv -> md_catchment_locations.csv`

| Total | linked | unlinked IDPs   Camps | unlinked Other |
|-------|--------|-----------------------|----------------|
| 50735 | 49806  | 136                   | 793            |

### IRS Reports `rd_irs_data.csv -> md_catchment_locations.csv`

| Total | linked | unlinked IDPs   Camps |unlinked Other |
|-------|--------|-----------------------|---------------|
| 30928 | 30188  | 140                   | 600           |
