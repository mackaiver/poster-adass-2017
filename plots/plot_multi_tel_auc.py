import click
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
from add_frame import add_frame


@click.command()
@click.argument('predicted_gammas', type=click.Path(exists=True, dir_okay=False,))
@click.argument('predicted_protons', type=click.Path(exists=True, dir_okay=False,))
@click.argument('output_file', type=click.Path(exists=False, dir_okay=False,))
def main(predicted_gammas, predicted_protons, output_file):
    '''
    Plot the event distributions from the triggered gammas given in the
    PREDICTED_EVENTS input file.
    '''

    gammas = pd.read_csv(predicted_gammas)
    gammas['true_label'] = 1

    protons = pd.read_csv(predicted_protons)
    protons['true_label'] = 0

    df = pd.concat([gammas, protons])

    y_score = df['prediction:signal:mean']
    y_true = df['true_label']

    fpr, tpr, _ = roc_curve(y_true, y_score)
    auc = roc_auc_score(y_true, y_score)

    plt.plot(fpr, tpr, lw=1, label='Total Area under Curve:${:.4f}$'.format(auc))
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    add_frame(plt.gca())
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file)


if __name__ == '__main__':
    main()
