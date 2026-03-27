import numpy as np

# Classifies into 0 or 1
def apply_threshold(scores, threshold):
    scores = np.asarray(scores, dtype=float)
    return (scores <= threshold).astype(int)


def confusion_counts(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_pred, dtype=int)

    if y_true.shape != y_pred.shape:
        raise ValueError("Both must have the same shape")
#True pos, true neg, false pos, false negs
    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))

    return {
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
    }

#num correct / total
def accuracy(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_pred, dtype=int)

    if y_true.shape != y_pred.shape:
        raise ValueError("Both must have the same shape")

    return float(np.mean(y_true == y_pred))

#Equal weight to both classes
#True pos + True neg / 2
def balanced_accuracy_from_counts(tp, tn, fp, fn):
    pos_denom = tp + fn
    neg_denom = tn + fp

    if pos_denom == 0 or neg_denom == 0:
        raise ValueError("Balanced accuracy is undefined")

    tpr = tp / pos_denom
    tnr = tn / neg_denom
    return float((tpr + tnr) / 2.0)


def balanced_accuracy(y_true, y_pred):
    counts = confusion_counts(y_true, y_pred)
    return balanced_accuracy_from_counts(
        counts["tp"], counts["tn"], counts["fp"], counts["fn"]
    )


def evaluate_predictions(y_true, y_pred):
    counts = confusion_counts(y_true, y_pred)
    acc = accuracy(y_true, y_pred)
    bal_acc = balanced_accuracy_from_counts(
        counts["tp"], counts["tn"], counts["fp"], counts["fn"]
    )

    return {
        "accuracy": acc,
        "balanced_accuracy": bal_acc,
        "tp": counts["tp"],
        "tn": counts["tn"],
        "fp": counts["fp"],
        "fn": counts["fn"],
    }