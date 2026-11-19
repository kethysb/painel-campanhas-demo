# Painel de campanhas

Projeto de análise de mídia paga com números fictícios. O script valida um CSV, agrupa as campanhas por canal e calcula CPC (custo por clique), CPL (custo por lead) e taxa de conversão (leads divididos por cliques).

Requer Python 3.10 ou mais recente, sem dependências externas. Execute:

```sh
python relatorio.py campanhas-exemplo.csv
```

O CSV deve conter `canal,investimento,cliques,leads`, com ponto como separador decimal. O investimento deve ser não negativo, e o número de leads deve estar entre zero e o número de cliques. Canais sem cliques ou leads recebem um traço na métrica correspondente.
